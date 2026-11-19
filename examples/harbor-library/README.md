# Harbor Library example

This fictional project demonstrates source-backed project memory across two sessions. Copy the entire [`workspace`](workspace) directory, including its `.atlas` profile, to a disposable folder. Open it as a project in your agent. If your host requires a Git project, run `git init` in the copy. The example works with ordinary Markdown lookup.

## Session 1

> Use Atlas Notes in this workspace. Read the project handoff and source policy. Save the current hold expiry decision under Decisions, including the reason and a link to the original policy. Report which file you updated.

Expect the decision note to explain that holds expire **48 hours after the pickup notification** so uncollected items return to circulation for the next reader. It should cite the **Pickup window** section of the [fixture policy](workspace/Sources/Desk%20Policy.md).

## Session 2

Start a fresh chat from the same copied workspace.

> Use Atlas Notes to tell me when reservations expire and why. Cite the decision note and the original policy section. This is read-only.

Expect the same rule and rationale with both sources. The second session should leave the Markdown and profile as they were after session 1.
