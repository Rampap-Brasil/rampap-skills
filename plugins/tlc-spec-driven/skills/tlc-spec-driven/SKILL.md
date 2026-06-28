---
name: tlc-spec-driven
description: Feature planning and implementation with 4 adaptive phases — Specify, Design, Tasks, Execute. Auto-sizes depth by complexity. Creates atomic tasks with verification criteria, atomic git commits, and requirement traceability. Features an independent Verifier (author != verifier, evidence-or-zero), persistent decision log (STATE.md), and test-coverage-matrix-driven tests, plus a self-improving lessons layer that turns verification failures into reusable project-local guidance. Stack-agnostic. Use when (1) Planning features (requirements, design, task breakdown), (2) Implementing with verification and atomic commits, (3) Validating or verifying an implementation against a spec. Triggers on "specify feature", "discuss feature", "design", "tasks", "implement", "validate", "verify work", "UAT", "record decision", "pause work", "resume work". Do NOT use for architecture decomposition analysis (use architecture skills) or technical design docs (use create-technical-design-doc).
license: CC-BY-4.0
metadata:
  type: shim
  upstream: "@tech-leads-club/agent-skills-mcp (skill: tlc-spec-driven)"
  upstream_author: "Felipe Rodrigues - github.com/felipfr"
  canonical_version_seen: "3.1.0"
---

# tlc-spec-driven (shim → MCP `agent-skills`)

This file is only a pointer. The canonical, always-current content of this skill lives in the
remote catalog served by the `agent-skills` MCP (Tech Lead's Club) — never here — so it can't go
stale. None of the skill's `references/` files are vendored, on purpose.

## Step 0 — Ensure the dependency (bootstrap; run this before anything else)

1. Check whether the MCP tool `mcp__agent-skills__read_skill` is available in this session
   (equivalently, run `claude mcp list` and look for `agent-skills ... ✔ Connected`).
2. If it is available, go to Step 1.
3. If it is NOT available, do not try to load the skill yet:
   - This plugin ships a correct `.mcp.json` that registers the `agent-skills` server, but MCP
     tools only enter a session at boot. Tell the user (in their language) what is happening and
     ask them to run `/reload-plugins` (or restart the session), then re-run this skill.
   - If it is still unavailable after a reload, run the fallback setup skill
     `tlc-spec-driven:setup` (it registers the MCP at user scope and verifies the connection).
     Then stop and ask the user to re-run this skill once setup reports `✔ Connected`.

## Step 1 — Load the real skill

1. Call `mcp__agent-skills__read_skill` with `{ "skill_name": "tlc-spec-driven" }`.
   It returns `[0]` the canonical SKILL.md and `[1]` the list of reference files.
2. Load references on demand with `mcp__agent-skills__fetch_skill_files`, using `skill_name:
   "tlc-spec-driven"` and only the exact `file_paths` from that list — never invent paths.
3. Follow the loaded instructions, applying the user's request. Communicate with the user in
   their preferred language (pt-BR).
