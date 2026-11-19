# Scoped retrieval
1. Resolve workspace and project; identify what decision the question needs.
2. Read current project context/handoff. Historical journals are evidence, not default instructions.
3. Exact lookup: use the host’s search within the workspace and profile scope, or use an existing Atlas catalog. Relationship question: use [the Graphify handoff](graphify.md) to resolve and check the scoped graph, then query it with an initial budget of about 1500 tokens. Narrow before expanding. Do not dump graph.json or the whole catalog.
4. Open the few relevant notes and source locations. Check version, scope and contrary evidence. An absent path does not prove independence.
5. Answer with sources, limits and gaps. For implementation context include current constraints, decisions, evidence, acceptance scenarios and live checks required.
6. Stop when the evidence answers the question. Query alone does not authorize note writes or external research beyond its scope.

Generic helper: python scripts/atlas.py search ROOT QUERY --limit 5. It ranks current, in-scope Markdown and compares its fingerprints to a previously built local catalog. The search runs locally and leaves files untouched. Prefer a mature workspace's native search when present. IDs/titles are entry points, not substitutes for reading evidence.
Graph freshness includes changes, renames, deletions and failed extraction. If stale or missing, use direct source retrieval, or refresh when the task authorizes it.
