# Optional Graphify integration

Use the installed upstream [Graphify skill and CLI](https://github.com/Graphify-Labs/graphify). Graphify’s code extraction and its semantic processing of notes or media have different coverage and costs. Check the installed version and supported input formats.

## Use an existing graph

1. Identify the exact graph for the selected workspace from its guidance, configured output, or build record. Check that the requested sources were indexed and that the graph reflects material changes. If available, use `python scripts/atlas.py status "WORKSPACE"` from the skill folder to check Atlas’s recorded scope. Supplement it with Graphify’s native indicators as needed.
2. Run a focused query. For example, run `graphify query "How is hold expiry applied?" --graph PATH_TO_GRAPH_JSON --budget 1500`. Use the installed version’s help for scope, path, and output controls. Narrow the query if the result is larger than needed.
3. Verify decisive claims in the original files. Preserve the distinction between explicit connections, inferred connections, and ambiguous matches. A missing, partial, or stale graph calls for direct retrieval unless the user authorizes a refresh.

## Build or refresh when authorized

Give Graphify the intended workspace, allowed paths from `graph_scope` or the task, exclusions, and output location. Run its supported workflow for the actual input types. Keep generated artifacts separate from the notes. Check the resulting graph and report paths, included and skipped files, extraction failures, and scope. Code-only extraction cannot establish coverage of Markdown or media.

When coverage is verified, optionally record hashes for explicit paths with the Atlas helper:

```sh
python scripts/atlas.py stamp "WORKSPACE" --files "path/to/source.md" --graph "graphify-out/graph.json" --evidence "graphify-out/GRAPH_REPORT.md"
python scripts/atlas.py status "WORKSPACE"
```

The stamp tracks only the listed files and recorded graph. For directories and patterns, also check newly added inputs against Graphify’s inventory. If a refresh fails, retain any useful last graph as stale and reopen the original evidence when needed.
