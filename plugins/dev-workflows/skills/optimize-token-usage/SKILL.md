---
name: optimize-token-usage
description: Use when a developer wants to cut Claude Code token/usage consumption or set up subagent delegation — "estou gastando muito token", "meus tokens vão acabar", "economizar tokens", "configurar subagentes em Sonnet", "/dev-workflows:optimize-token-usage". Audits the developer's personal Claude Code setup (default subagent model, delegation rule, enabled plugins, memory index size), applies fixes with backups after explicit confirmation, and explains the trade-offs. Touches only ~/.claude, never the repository.
---

# Optimize Claude Code token usage

Audit and tune the developer's **personal** Claude Code setup (`~/.claude/`) so they spend fewer
tokens without losing capability. Report to the user in their preferred language, briefly.

Validated on 2026-11-09 on a real setup: subagents moved to Sonnet, 18 unused plugins disabled,
memory index cut from 33 KB (truncated on load) to 19 KB.

## When NOT to use

- Changing a repository's shared `CLAUDE.md`, `.claude/agents/` or `.claude/settings.json` — those
  affect the whole team; propose them in a PR instead.
- Cleaning git branches — use `dev-workflows:clean-session-branches`.
- Updating plugins — use `plugin-updater:update-plugins`.

## Explain first: what actually saves tokens

Tell the user this before changing anything, so they understand what to expect:

1. **Fixed context is re-sent on every turn** — system prompt, CLAUDE.md files, the memory index,
   the skill/tool listings of every enabled plugin and connector, and text injected by hooks.
   Trimming it pays off on every message.
2. **Model choice** — Sonnet consumes less of the usage limit than Opus. Subagents on Sonnet; the
   main session on Sonnet for routine work (`/model sonnet`), Opus only for hard problems.
3. **Delegate selectively, not everything** — every subagent starts from zero and reloads the
   system prompt, CLAUDE.md and tool listings. It pays off for wide sweeps (many files, large logs,
   repo-wide searches), where what is read dwarfs the report that comes back. For a small task
   with a known target it costs MORE. Measured: compacting a single file through a subagent burned
   ~100k tokens and still needed a manual fix.
4. **Session hygiene** — `/clear` between unrelated tasks, `/compact` in long conversations,
   `/cost` or `/usage` to measure before and after.

## Step 1 — Audit (read-only)

```bash
# Default subagent model (empty = subagents inherit the session model, usually Opus)
python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude/settings.json'))).get('env',{}).get('CLAUDE_CODE_SUBAGENT_MODEL'))"
env | grep CLAUDE_CODE_SUBAGENT_MODEL

# Agents with their own model (frontmatter `model:` wins over the env var)
grep -nH '^model:' ~/.claude/agents/*.md .claude/agents/*.md 2>/dev/null

# Delegation rule in the personal CLAUDE.md
grep -n 'Token economy' ~/.claude/CLAUDE.md 2>/dev/null

# Enabled plugins
python3 -c "import json,os;d=json.load(open(os.path.expanduser('~/.claude/settings.json')));print('\n'.join(k for k,v in d.get('enabledPlugins',{}).items() if v))"

# Memory index of the current project (loaded up to ~24 KB; anything beyond is silently cut)
wc -c ~/.claude/projects/$(pwd | sed 's#[/.]#-#g')/memory/MEMORY.md 2>/dev/null
```

Present the findings as a short table and **ask for confirmation** before Step 2 — these files are
the user's own configuration.

## Step 2 — Apply (with backups, only what the user approved)

Back up first: `cp ~/.claude/settings.json ~/.claude/settings.json.bak-$(date +%F)`.

1. **Subagents on Sonnet** — merge into the existing `env` object of `~/.claude/settings.json`
   (keep other variables):
   ```json
   "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet" }
   ```
   Agents with their own `model:` keep it on purpose (e.g. a reviewer pinned to a stronger model).
   `fork` always runs on the main session's model, so it never saves tokens.
2. **Delegation rule** — append this section to `~/.claude/CLAUDE.md` (create the file if missing;
   never overwrite existing content). Keep it in English — it is an instruction for the model:
   ```markdown
   ## Token economy — subagent delegation

   Subagents run on Sonnet by default (`CLAUDE_CODE_SUBAGENT_MODEL=sonnet` in settings.json).

   - **Delegate** (Agent tool, preferably `Explore` or `general-purpose`) when the task requires
     reading many files, sweeping the repository, analyzing large logs/outputs, or repetitive
     mechanical work. The goal is to keep the main context lean and receive only the conclusion.
   - **Do not delegate** small tasks (known target, few files, pinpoint edit): spinning up an agent
     from scratch (system prompt + CLAUDE.md + tools) costs more than doing it directly.
   - **Never use `fork`** to save tokens: it always runs on the main session's model.
   - When delegating, ask for a short report (conclusion + `file:line`), no file dumps.
   - Do not run the same investigation in parallel with the agent it was delegated to.
   ```
3. **Plugins** — propose a list to disable and disable only what the user approves, by setting
   `enabledPlugins.<name> = false` through `python3` + `json` (preserves the rest of the file).
   Typical candidates: generic agents that duplicate others (e.g. several `*@cc-marketplace`
   agents, a second commit plugin), plugins unrelated to the user's stack, and plugins whose hooks
   inject text into every session without real use. Ask about anything the team relies on (e.g. a
   code-review plugin required by the project) before touching it.
4. **Memory index above ~20 KB** — do it **by hand, without a subagent** (one file, known target).
   Back up as `MEMORY.md.bak-<date>`, shorten each line to ~110 characters keeping the recall
   keywords (system, customer, date, state such as "in prod"), never drop an entry nor change the
   `file.md` of a link. Script-based truncation destroys the hooks that make recall work — don't.
   Validate (no output = nothing lost):
   ```bash
   diff <(grep -o '([a-z0-9-]*\.md)' MEMORY.md.bak-<date> | sort -u) <(grep -o '([a-z0-9-]*\.md)' MEMORY.md | sort -u)
   ```

After editing the JSON, validate it:
`python3 -c "import json,os;json.load(open(os.path.expanduser('~/.claude/settings.json')))"`.

## Step 3 — Outside Claude's reach (tell the user)

- **claude.ai connectors** and **account-level skills** add their tools/skills to every session;
  disable the unused ones in claude.ai → Settings → Connectors / Capabilities.
- `settings.json` changes take effect only in the **next session**.
- Measure: open a new session and run `/cost` or `/usage` on a task comparable to before.

## Rules

- Never edit `.env` files or any repository file through this skill.
- Never disable a plugin without explicit approval of the list.
- Always back up `~/.claude/settings.json` and `MEMORY.md` before editing them.
