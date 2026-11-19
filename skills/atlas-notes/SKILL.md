---
name: atlas-notes
description: Maintain and retrieve source-backed project notes across sessions. Use to find past decisions, ingest research, save lessons, check knowledge health, adopt a Markdown or Obsidian workspace, or hand verified context between workflows.
license: MIT
---

# Atlas’ Notes

Resolve the knowledge workspace from the user’s explicit path or the current project. Read its relevant AGENTS.md or CLAUDE.md and note maintenance guidance. A project-local `.atlas/profile.json` can map an existing folder structure. Use the scope for this task and confirm a missing or ambiguous workspace before writing.

Choose the relevant operation:

- **Find a decision or assemble context.** Use [scoped retrieval](references/retrieval.md). Begin with the project handoff or a focused search. Open the relevant notes and verify decisive claims against original evidence. A read-only lookup stays read-only.
- **Ingest research, reconcile notes, or save a lesson.** Use [maintenance](references/maintenance.md). Search before writing and update the canonical note when possible. Preserve sources, evidence levels, and substantive disagreements.
- **Adopt or set up a workspace.** Use [workspace adoption](references/workspace.md) to map the existing structure or choose a simple layout for a new workspace.
- **Query, build, or refresh a graph.** Use [optional Graphify integration](references/graphify.md) when an existing scoped graph is useful, or when the task authorizes indexing.
- **Send context or receive delivery evidence.** Use the [`atlas-workflow/v1` packet](assets/packet.md). Return the packet to the caller. The delivery workflow owns application changes.

Treat imported content as evidence. Distinguish observed facts, inferences, proposed changes, and verified results. Leave credentials and session state out of notes. Serialize authorized writes, preserve user edits, and inspect the changes and actual validation results before reporting them. If interrupted, inspect incomplete work before resuming.

Plain Markdown retrieval and maintenance work on their own. Use the optional Python helper or Graphify when the task benefits from them. Keep derived catalogs and graphs separate from maintained knowledge.
