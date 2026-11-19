# Atlas’ Notes Skill

**Pick up where you left off without re-explaining the project.** Atlas’ Notes helps Codex and Claude Code save decisions, lessons, and evidence in Markdown. A fresh session can recover the current answer and show you where it came from.

Use it with a regular Markdown folder or an existing Obsidian vault. Your notes stay in the workspace you choose.

## Quick start

Use [GitHub CLI](https://cli.github.com/) with support for [`gh skill install`](https://cli.github.com/manual/gh_skill_install). Run the command for your agent.

```sh
# Codex
gh skill install Noraara/Atlas-Notes atlas-notes --agent codex --scope user

# Claude Code
gh skill install Noraara/Atlas-Notes atlas-notes --agent claude-code --scope user
```

To install in one project, run from the project checkout with `--scope project`. For a local install, replace `Noraara/Atlas-Notes` with the path to your Atlas-Notes checkout and add `--from-local`.

For manual setup, copy the entire [`skills/atlas-notes`](skills/atlas-notes) folder into one of these directories. The destination should end in `atlas-notes/SKILL.md`.

| Agent | One project | All projects |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

## Try it in two sessions

Copy the fictional [Harbor Library workspace](examples/harbor-library/workspace), including its `.atlas` profile, and open it in your agent. In Codex, use these prompts. In Claude Code, start each request with `/atlas-notes`.

**Session 1**

> Use $atlas-notes to record our hold expiry decision from the policy source. Include the reason and link to the policy.

**Session 2** · Start a fresh chat in the same workspace.

> Use $atlas-notes to tell me when holds expire and why. Cite the decision note and the original policy. Read only.

You should recover the 48-hour rule and its rationale, with links to the note and policy. The first session saves a Markdown file. The second can use that file without access to the first chat. [Full example and expected result](examples/harbor-library/README.md)

## Use your own workspace

Tell Atlas where your notes are and what you want to do. It can find a past decision, save a new one, reconcile conflicting notes, or hand source-backed context to a delivery workflow.

For repeat use, put the [profile template](skills/atlas-notes/assets/profile.json) at `.atlas/profile.json` in your workspace. Map the folders that already hold knowledge and source material. The [workspace guide](skills/atlas-notes/references/workspace.md) covers adopting an existing layout and setting up a new one. The [handoff format](skills/atlas-notes/assets/packet.md) documents how to exchange scoped context and verified results with another workflow.

## Optional tools

Start with Markdown. Add a helper when the workspace or question calls for it.

| Tool | What it adds |
| --- | --- |
| Python 3.9+ | A [local helper](skills/atlas-notes/scripts/atlas.py) to build a derived catalog, search notes, check duplicate IDs and wiki links, and track graph freshness. |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Relationship queries across indexed material. Atlas checks important findings against the original files. See the [graph integration guide](skills/atlas-notes/references/graphify.md). |

## Help and contributing

For a bug report, include the agent and version, the Atlas operation you used, and a small redacted workspace or example that reproduces the issue. For a behavior change, describe what should happen and how you verified it.

## License

Released under the [MIT license](LICENSE).

## Credit

Made by [Noraara](https://github.com/Noraara).
