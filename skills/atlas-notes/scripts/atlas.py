"""Bounded local Markdown index and explicit graph freshness. Standard library only."""
from pathlib import Path
import argparse, hashlib, json, os, re, tempfile

SKIP = {".git", ".obsidian", ".atlas", "graphify-out", "node_modules", "__pycache__", ".venv"}
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def atomic_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".atlas-write-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)
def inside(root, value):
    p = (root / value).resolve()
    if not p.is_relative_to(root): raise ValueError("Path escapes workspace: " + str(value))
    return p
def profile_paths(root, profile, key, default):
    values = profile.get(key, default)
    if not isinstance(values, list) or any(not isinstance(p, str) or not p for p in values):
        raise ValueError(f"Profile {key} must be a list of workspace-relative paths")
    if any(Path(p).anchor for p in values):
        raise ValueError(f"Profile {key} must use workspace-relative paths")
    return [inside(root, p) for p in values]

def local_artifact(root, filename):
    path = root / ".atlas" / filename
    if path.resolve() != path:
        raise ValueError(f"Atlas artifact must use its workspace path: {filename}")
    return path

def notes(root, included, excluded):
    def permitted(path):
        return not any(path.is_relative_to(skip) for skip in excluded)

    for directory, dirs, files in os.walk(root, followlinks=False):
        base = Path(directory)
        dirs[:] = sorted(
            name for name in dirs
            if name not in SKIP and not name.startswith(".")
            and not (base / name).is_symlink()
            and (base / name).resolve() == base / name
            and permitted(base / name)
            and any((base / name).is_relative_to(target) or target.is_relative_to(base / name)
                    for target in included)
        )
        for name in sorted(files):
            path = base / name
            if path.suffix.lower() != ".md" or name in {"AGENTS.md", "CLAUDE.md"}:
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                continue
            if permitted(path) and any(path.is_relative_to(target) for target in included):
                yield path
def scalar(text, key):
    if not text.startswith("---\n") and not text.startswith("---\r\n"): return ""
    front=text.split("---",2)[1]
    match=re.search(r"^"+key+r":\s*(.+)$",front,re.M)
    return match.group(1).strip().strip('"').strip("'") if match else ""
def rows(root):
    result=[]
    profile_path = local_artifact(root, "profile.json")
    profile = json.loads(profile_path.read_text(encoding="utf-8-sig")) if profile_path.exists() else {}
    if not isinstance(profile, dict):
        raise ValueError("Workspace profile must be a JSON object")
    included = profile_paths(root, profile, "knowledge_roots", ["."])
    excluded = profile_paths(root, profile, "exclude", [])
    for p in notes(root, included, excluded):
        text=p.read_text(encoding="utf-8-sig")
        heading=re.search(r"^# (.+)$",text,re.M)
        title=scalar(text,"title") or (heading.group(1) if heading else p.stem)
        result.append(dict(path=p.relative_to(root).as_posix(), title=title, id=scalar(text,"id"), summary=scalar(text,"summary"), sha256=digest(p), text=text))
    return result
def errors(root, data):
    out=[]; ids={}; names={}
    for r in data:
        if r["id"]:
            if r["id"] in ids: out.append("duplicate id: "+r["id"])
            ids[r["id"]]=r["path"]
        for name in {r["title"],Path(r["path"]).stem}:
            names.setdefault(name, set()).add(r["path"])
    paths={r["path"] for r in data}
    for r in data:
        for target in re.findall(r"\[\[([^\]]+)\]\]",r["text"]):
            target=target.split("|")[0].split("#")[0]
            if not target: continue
            if target in names:
                if len(names[target])>1: out.append(r["path"]+": ambiguous link "+target)
                continue
            path=target if target.endswith(".md") else target+".md"
            if path in paths: continue
            # Existing assets or relative links can be non-Markdown.
            try:
                if inside(root,target).exists() or inside(root,str(Path(r["path"]).parent/target)).exists(): continue
            except ValueError: pass
            out.append(r["path"]+": unresolved link "+target)
    return out
def main():
    p=argparse.ArgumentParser()
    p.add_argument("command",choices=["index","search","check","stamp","status"])
    p.add_argument("root")
    p.add_argument("query",nargs="?",default="")
    p.add_argument("--limit",type=int,default=5)
    p.add_argument("--files",nargs="+")
    p.add_argument("--graph")
    p.add_argument("--evidence")
    a=p.parse_args(); root=Path(a.root).resolve()
    if not root.is_dir(): raise ValueError("Workspace does not exist")
    if a.command in ("index","check","search"):
        data=rows(root)
        if a.command=="index":
            problems=errors(root,data)
            if problems:
                print(json.dumps({"errors":problems},indent=2)); return 1
            atomic_json(local_artifact(root, "catalog.json"),{"schema":"atlas-index/v1","notes":data})
            print(json.dumps({"indexed":len(data)})); return 0
        if a.command=="check":
            problems=errors(root,data)
            print(json.dumps({"notes":len(data),"errors":problems},indent=2)); return bool(problems)
        index=local_artifact(root, "catalog.json")
        if not index.exists(): raise ValueError("No index. Use native search or explicitly build one.")
        old=json.loads(index.read_text(encoding="utf-8"))["notes"]
        stale={r["path"]:r["sha256"] for r in old}!={r["path"]:r["sha256"] for r in data}
        terms=set(re.findall(r"\w+",a.query.casefold()))
        ranked=[]
        for r in data:
            score=sum(5*(t in r["title"].casefold())+2*(t in r["summary"].casefold())+(t in r["text"].casefold()) for t in terms)
            if score: ranked.append((score,r))
        ranked.sort(key=lambda v:(-v[0],v[1]["path"]))
        print(json.dumps({"index_stale":stale,"results":[{k:r[k] for k in ("path","title","summary")} for _,r in ranked[:max(1,a.limit)]]},indent=2))
        return 0
    manifest=local_artifact(root, "graph-scope.json")
    if a.command=="stamp":
        if not a.files or not a.graph or not a.evidence: raise ValueError("stamp requires --files --graph --evidence")
        graph=inside(root,a.graph); evidence=inside(root,a.evidence)
        parsed=json.loads(graph.read_text(encoding="utf-8-sig"))
        if not isinstance(parsed,dict) or not isinstance(parsed.get("nodes"),list): raise ValueError("Invalid graph")
        if not evidence.is_file(): raise ValueError("Build evidence missing")
        fingerprints={str(inside(root,x).relative_to(root)).replace("\\","/"):digest(inside(root,x)) for x in a.files}
        atomic_json(manifest,dict(schema="atlas-graph-scope/v1",files=fingerprints,graph=graph.relative_to(root).as_posix(),graph_sha256=digest(graph),evidence=evidence.relative_to(root).as_posix()))
        print(json.dumps({"stamped_files":len(fingerprints),"scope":"explicit-files-only"})); return 0
    if not manifest.exists():
        print(json.dumps({"state":"missing","coverage":"unknown"})); return 1
    m=json.loads(manifest.read_text(encoding="utf-8")); changed=[]
    for f,h in m["files"].items():
        path=inside(root,f)
        if not path.is_file() or digest(path)!=h: changed.append(f)
    graph=inside(root,m["graph"])
    graph_changed=not graph.is_file() or digest(graph)!=m["graph_sha256"]
    print(json.dumps({"state":"stale" if changed or graph_changed else "current","changed":changed,"graph_changed":graph_changed,"coverage":"explicit-files-only","indexed_files":len(m["files"])},indent=2))
    return int(bool(changed or graph_changed))
if __name__=="__main__":
    try: raise SystemExit(main())
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e:
        print(json.dumps({"error":str(e)})); raise SystemExit(2)
