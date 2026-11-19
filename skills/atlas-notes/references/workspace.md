# Workspace adoption

Choose one project or knowledge folder for the task. Find its current handoff, source register, and maintenance guidance before opening unrelated folders.

For an existing Markdown collection or Obsidian vault, preserve its folders, IDs, metadata, links, and validator. If repeated use benefits from a stable mapping, copy the [profile template](../assets/profile.json) to `.atlas/profile.json` and edit the paths relative to the workspace root. Use the profile to locate project notes and original sources. A workspace validator is a reference to review before use. The helper does not execute commands from profiles.

For a new workspace, start with what the project needs. Use Projects for active outcomes, Areas for ongoing responsibilities, Resources for reusable reference material, and Archive for inactive material. Inbox and Sources can hold material to review and original evidence. Use [the project handoff](../assets/project-profile.md) if one is missing and [the note template](../assets/note.md) when there is no local convention.

## Optional Python helper

Run these commands with Python 3.9+ from the installed skill folder, substituting the path to the selected workspace for `WORKSPACE`.

```sh
python scripts/atlas.py check "WORKSPACE"
python scripts/atlas.py index "WORKSPACE"
python scripts/atlas.py search "WORKSPACE" "hold expiry" --limit 5
```

`check` validates duplicate IDs and wiki-link targets within the supported conventions. Use the native validator when a vault uses additional linking rules. `index` validates and writes a derived `.atlas/catalog.json`. `search` needs a previously built catalog, ranks the current in-scope Markdown, and reports whether its fingerprints differ from that catalog. Use native search when there is no catalog. A profile limits which note roots are scanned via `knowledge_roots` and can exclude additional workspace-relative paths. Without a profile, the helper uses the explicitly selected workspace and skips common generated directories. The catalog is local and derived. Keep it out of public commits if it contains private project metadata.

Creating a workspace, building an index, and editing notes are separate operations. Resolve missing workspace paths with the user before creating anything.
