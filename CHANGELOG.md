# Changelog

All notable changes to the **Rampap Skills** marketplace are documented in this file.

This is a monorepo: each plugin is versioned independently, so changes are grouped by
plugin. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Conventions: `Added` = new features, `Changed` = changes to existing behavior,
> `Fixed` = bug fixes, `Removed` = removed features.

---

## design-system

### [1.0.1] — 2026-02-25
#### Changed
- Maintenance bump after repo reorganization for multi-plugin support.

#### Fixed
- Moved `plugin.json` to `.claude-plugin/` and updated the install command.

### [1.0.0] — 2026-02-25
#### Added
- Initial `design-system` plugin with the `setup`, `add-component`, and `build-page` skills
  (setup from a visual reference, add shadcn/custom components, build pages from screenshots/Figma).
- First version of the `rampap-skills` marketplace.

---

## plugin-updater

### [1.1.0] — 2026-02-25
#### Changed
- Improved the `update-plugins` skill with Windows compatibility and an explicit
  marketplace pull before updating.

### [1.0.0] — 2026-02-25
#### Added
- Initial plugin (originally named `plugin-manager`) with the `update-plugins` and
  `update-skills` skills.
#### Changed
- Renamed the plugin from `plugin-manager` to `plugin-updater`.

---

## marketing-campaigns

### [0.2.0] — 2026-06-28
#### Added
- `--lang` flag on `etl_mrp.py`: runtime logs are emitted in the user's preferred language
  (default `pt-BR`, English fallback).
#### Changed
- Translated all source files (SKILL.md, references, `plugin.json`) to English, keeping
  external data identifiers (Sankhya MRP column names, template sheet names) verbatim.
#### Fixed
- Synced the marketplace description to English (it had been left in Portuguese).
- Fixed `str | None` type hints failing on Python 3.9 (`from __future__ import annotations`).

### [0.1.0] — 2026-03-29
#### Added
- Initial `marketing-campaigns` plugin with the `etl` skill: transforms a raw Sankhya MRP
  export into Rampap's PRs Campaign template, filtering inactive and out-of-stock products.

---

## dev-workflows

### [1.0.1] — 2026-06-28
#### Changed
- Translated the `clean-session-branches` skill to English; output instructions now follow
  the user's preferred language dynamically (instead of hardcoded pt-BR).

### [1.0.0] — 2026-06-28
#### Added
- Initial `dev-workflows` plugin with the `clean-session-branches` skill: two-phase local
  git branch cleanup (safe auto-cleanup of session branches merged into `develop`, plus
  opt-in sanitization of the remaining merged branches).
