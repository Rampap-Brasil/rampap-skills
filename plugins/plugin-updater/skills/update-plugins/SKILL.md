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
- `version` — currently installed version
- `installPath` — cache location
- `lastUpdated` — timestamp of last update

### 2. Check for available updates

For each marketplace, the local git clone lives at `~/.claude/plugins/marketplaces/<marketplaceName>/`.

For each installed plugin:

1. Run `git fetch origin` in the marketplace directory (lightweight — only fetches refs)
2. Read the remote plugin.json to get the latest version:

```bash
git -C ~/.claude/plugins/marketplaces/<marketplaceName>/ show origin/main:plugins/<pluginName>/.claude-plugin/plugin.json
```

3. Parse the `version` field from the remote JSON and compare with the installed version.

If `git show` fails (different branch name or path structure), try `origin/master` as fallback. If both fail, mark the plugin as "unable to check".

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
 >>  3  superpowers@superpowers-dev                 4.2.0            4.3.0            user
  ?  4  interface-design@interface-design           2026.2.8.2129    —                local
     ...
```

Then ask the user:

> Which plugins do you want to update?
> - **all** — update all plugins with available updates
> - **1,3** — update specific plugins by number
> - **none** — cancel

Wait for the user's response before proceeding.

### 4. Update selected plugins

For each selected plugin, run:

```bash
claude plugin update "<pluginName@marketplaceName>" --scope <scope>
```

Use the `scope` from the plugin's own entry. If a plugin has multiple entries with different scopes, update each one separately.

### 5. Present a summary

Show results:

```
Results:
  Updated:           2  (design-system 1.0.1 -> 1.1.0, superpowers 4.2.0 -> 4.3.0)
  Already latest:   12
  Failed:            1  (interface-design — not installed at scope user)
```

### 6. Remind to restart

Tell the user to **restart Claude Code** to apply the changes.

## Notes

- On Windows, `claude` CLI may not work from within Claude Code's bash tool. If commands fail silently, provide the user a PowerShell script to paste in their terminal. Adapt the script to only include the plugins they selected.

- `claude plugin update` requires a version bump in `plugin.json` to detect changes. If code changed but version didn't, it reports "already at latest version".

- The `git fetch` + `git show` approach is lightweight — it only downloads git refs, not full file contents.
