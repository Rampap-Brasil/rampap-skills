---
name: update-plugins
description: Update all installed Claude Code plugins at once. Use when the user wants to update, refresh, or sync their installed plugins to the latest versions.
---

# Update All Plugins

Check for updates and selectively update installed Claude Code plugins.

## Steps

### 1. Read the plugin registry

Read `~/.claude/plugins/installed_plugins.json`.

Parse the JSON. Each key in `plugins` follows the format `pluginName@marketplaceName`. Each entry has:
- `scope` — `user`, `project`, or `local`
- `version` — currently installed version (may be a semver OR a git SHA prefix)
- `installPath` — cache location
- `gitCommitSha` — full SHA of the marketplace commit when plugin was installed
- `projectPath` — (only for `local` scope) the project directory this plugin is bound to

### 2. Check for available updates

For each unique marketplace, the local git clone lives at `~/.claude/plugins/marketplaces/<marketplaceName>/`.

For each marketplace (deduplicated):

1. Run `git fetch origin` in the marketplace directory (lightweight — only fetches refs)

For each installed plugin in that marketplace:

2. Resolve the remote HEAD hash first, then read plugin.json from it:

```bash
HASH=$(git -C ~/.claude/plugins/marketplaces/<marketplaceName>/ rev-parse origin/main)
git -C ~/.claude/plugins/marketplaces/<marketplaceName>/ show "$HASH:plugins/<pluginName>/.claude-plugin/plugin.json"
```

**Why use `$HASH:path` instead of `origin/main:path`:** On Windows, `git show origin/main:.claude-plugin/...` gets mangled (the colon + dot becomes `origin\main;.claude-plugin\...`). Using the resolved hash avoids this.

3. If the above fails, try the root-level path (some plugins aren't under `plugins/`):

```bash
git -C ~/.claude/plugins/marketplaces/<marketplaceName>/ show "$HASH:.claude-plugin/plugin.json"
```

4. If both fail, try `origin/master` as the branch. If all fail, mark as "unable to check".

5. Compare versions:
   - **If remote plugin.json has a `version` field:** compare it with the installed `version`.
   - **If remote plugin.json has NO `version` field:** compare the latest marketplace commit SHA (`$HASH`) with the installed `gitCommitSha`. If they differ, an update is available.

### 3. Present the plugin list for selection

Display a numbered table showing installed vs available versions. Use an update indicator:

- `>>` — update available
- (blank) — already at latest
- `?` — unable to check

```
     #  Plugin                                     Installed        Available        Scope
     ── ────────────────────────────────────────── ──────────────── ──────────────── ─────────
 >>  1  design-system@rampap-skills                1.0.1            1.1.0            user
     2  frontend-design@claude-plugins-official     55b58ec6e564     55b58ec6e564     user
 >>  3  superpowers@superpowers-dev                 4.2.0            4.3.1            user
 >>  4  interface-design@interface-design           2026.2.8.2129    2026.2.9.1212    local
     ...
```

Then ask the user:

> Which plugins do you want to update?
> - **all** — update all plugins with available updates
> - **1,3** — update specific plugins by number
> - **none** — cancel

Wait for the user's response before proceeding.

### 4. Update selected plugins

#### 4a. Pull marketplace repos

For each marketplace that has plugins to update, pull the latest code into the local checkout:

```bash
git -C ~/.claude/plugins/marketplaces/<marketplaceName>/ pull origin main
```

This is required because `claude plugin update` reads from the local checkout, not from remote refs. Without pulling, it will report "already at latest version" even when updates exist.

#### 4b. Run update commands

**On Windows:** The `claude` CLI does not work from within Claude Code's bash tool. Skip trying the CLI and go directly to providing a PowerShell script for the user to paste in their terminal.

**On macOS/Linux:** Run the CLI commands directly:

```bash
claude plugin update "<pluginName@marketplaceName>" --scope <scope>
```

**PowerShell script format (Windows):**

```powershell
# Pull marketplace updates
cd "$env:USERPROFILE\.claude\plugins\marketplaces\<marketplaceName>"
git pull origin main

# Update plugin
cd <directory>
claude plugin update "<pluginName@marketplaceName>" --scope <scope>
```

**Important for `local`-scoped plugins:** The update command must be run from the plugin's `projectPath` directory (from `installed_plugins.json`), otherwise it fails with "not installed at scope local".

For `user`-scoped plugins, the directory doesn't matter (use `~` or `$env:USERPROFILE`).

### 5. Present a summary

Show results:

```
Results:
  Updated:          2  (superpowers 4.2.0 -> 4.3.1, interface-design 2026.2.8.2129 -> 2026.2.9.1212)
  Already latest:  15
  Unable to check:  1  (some-plugin — path not found in remote)
```

### 6. Remind to restart

Tell the user to **restart Claude Code** to apply the changes.

## Notes

- `claude plugin update` requires a version bump in `plugin.json` to detect changes. If code changed but version didn't, it reports "already at latest version".

- The `git fetch` + `git show` approach is lightweight for version checking — it only downloads git refs, not full file contents. The `git pull` is only needed in step 4a for marketplaces with actual updates.

- When comparing SHA-based versions (plugins without a `version` field), compare `gitCommitSha` from the registry against the latest remote SHA — the short SHA shown as `version` is just a display prefix.
