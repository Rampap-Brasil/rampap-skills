---
name: clean-session-branches
description: Use when the user wants to clean up local git branches after merging work into develop — deletes branches created during this conversation that are already merged into develop, then offers the remaining merged branches for explicit, opt-in deletion. Local branches only; never touches protected/long-lived branches (main, master, develop, sandbox, staging, homolog, production, qa) or the current branch.
---

# Clean up session branches

Cleans **local** branches in two phases: safe automation for what I created myself in this
conversation and that is already merged, and opt-in sanitization for the rest. Never uses
`git branch -D` (force) — always `git branch -d`, which refuses to delete unmerged work.

## When NOT to use

- To remove **remote** branches or prune `refs/remotes/*` — this skill is deliberately
  *local-only*. Use `git push origin --delete <branch>` / `git remote prune origin` manually.
- To delete **unmerged** branches or force deletion (`git branch -D`) — this skill never
  forces; unpublished work is preserved by design.

## Preconditions

1. Confirm you are inside a git repository: `git rev-parse --is-inside-work-tree`.
2. Confirm the `develop` branch exists: `git rev-parse --verify develop`. If it does not exist,
   ask the user which branch is the base before continuing.

## Guard-rails (apply to both phases)

- **Protected branches — NEVER delete**, in either phase, even if they show up as merged.
  The list (case-insensitive) is:
  - the base branch (`develop` or the one given in the preconditions) and `main`/`master`;
  - environment/long-lived branches: `sandbox`, `staging`, `homolog`, `homologacao`,
    `production`, `prod`, `qa`;
  - the branch currently checked out (`git branch --show-current`).
- **Never** force deletion. Operate **only on local branches** — do not touch remotes or
  `refs/remotes/*`.
- Always use `git branch -d <name>` (safe delete). If git refuses (not merged, or merged into
  HEAD but ahead of its own upstream), **do not** force — report it and move on.

## Phase 1 — Auto-cleanup (no confirmation)

1. **Build the session candidate list.** Re-read THIS conversation and identify the branches that
   **I (Claude) created** in it, looking for commands I ran such as `git checkout -b <name>`,
   `git switch -c <name>`, and `git branch <name>`. This is the `created_in_session` list.
2. **Intersect with merged branches.** Run `git branch --merged develop --format='%(refname:short)'`.
   The candidates are `created_in_session ∩ merged`.
3. **Resolve the current branch.** If the checked-out branch is among the candidates, run
   `git switch develop` before deleting (and remove it from the list per the guard-rails above).
4. **Delete** each candidate with `git branch -d <name>`.
5. **Report** in the user's preferred language: which branches were deleted and which were skipped
   (with the reason, e.g. "git refused — not fully merged").

## Phase 2 — Sanitization (explicit user choice)

6. **Compute the remainder.** Take `git branch --merged develop --format='%(refname:short)'` and
   remove: the ones deleted in Phase 1, all **protected branches** (see Guard-rails), and anything
   already covered.
7. If **nothing is left**, tell the user there is nothing more to sanitize and finish.
8. If something remains, **list** each leftover branch with metadata useful for the decision.
   Suggested collection per branch:
   - last commit date: `git log -1 --format='%ci' <name>`
   - last commit author: `git log -1 --format='%an' <name>`
9. **Ask the user** which of these to delete. The default is **none** — do not delete anything
   from Phase 2 without an explicit choice.
10. **Delete** the chosen ones with `git branch -d <name>` and **report** the result in the user's
    preferred language.

## Closing

If Phase 1 and Phase 2 both have nothing to do, report "Nothing to clean." and finish.

## Notes

- `git branch --merged` only detects merges that preserve history (merge commit or fast-forward).
  With *squash/rebase merge* the branch does not show as merged — for safety, the skill
  (correctly) will not delete it.
- If the conversation is very long and the context was compacted, I may not see branches created
  near the very beginning; they simply reappear in Phase 2 for the user to choose, instead of
  being lost.
- **Merged into HEAD but ahead of upstream:** `git branch -d` refuses to delete a branch that is
  merged into `develop` but has local commits not yet pushed to its `origin/<branch>` (message
  "not yet merged to refs/remotes/origin/..."). This is expected — report it as skipped (local
  commits not published) and **do not** force; the user can resolve it manually.
- **Branch in use by another worktree:** `git branch -d` also refuses to delete a branch that is
  checked out in another worktree. Report it as skipped (in use at `<path>`) and move on.
