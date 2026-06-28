# Rampap Skills — Project Conventions

## Repository Structure

```
rampap-skills/
├── .claude-plugin/
│   └── marketplace.json        # Marketplace registry — lists all plugins
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json      # Plugin metadata (name, version, author)
│       └── skills/
│           └── <skill-name>/
│               ├── SKILL.md     # Skill instructions (required)
│               └── ...          # Bundled resources (scripts/, references/, assets/)
├── CLAUDE.md                    # This file
└── README.md
```

## Adding a New Plugin

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json` with name, description, version, author
2. Add skills under `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`
3. Register the plugin in `.claude-plugin/marketplace.json` under the `plugins` array with `"source": "./plugins/<plugin-name>"`

## Adding a New Skill to an Existing Plugin

1. Create `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`
2. Include YAML frontmatter with `name` and `description`
3. Add bundled resources as needed (templates, scripts, references)

## Skill Naming

- Plugin name = top-level identifier (e.g., `design-system`)
- Skill name = action identifier (e.g., `setup`, `add-component`, `build-page`)
- Invocation pattern: `<plugin-name>:<skill-name>`

## Language Convention

These skills are built for Rampap's Portuguese-speaking staff. The guiding principle is
**"write for your audience": human-facing material is Portuguese (pt-BR); only what an AI agent
consumes as instructions stays in English** (LLMs follow English instructions most reliably).

- **Agent-facing prompts → English.** The `SKILL.md` body, the `SKILL.md` frontmatter
  `description` (the trigger text the model reads to decide when to invoke a skill), the bundled
  `references/` files (loaded into the agent's context), and this `CLAUDE.md` are all agent
  instructions and must be in English.
- **Human-facing content → Portuguese (pt-BR).** `README.md`, `CHANGELOG.md`, the `description`
  fields in `plugin.json` / `marketplace.json` (shown to people browsing the marketplace), and
  code comments / docstrings (read by the pt-BR-speaking team maintaining the code).
- **Runtime output and generated logs → the user's preferred language (pt-BR).** Phrase skill
  instructions dynamically (e.g. "report in the user's preferred language"). Scripts that print
  logs localize via a message table + a `--lang` flag (default `pt-BR`, English fallback).
- **Identifiers always stay in English** (this is a universal convention, not prose): code
  identifiers (variables, functions, JSON keys) and external data identifiers that scripts/ETL
  match against — e.g. Sankhya MRP column names (`Ativo`, `Em ruptura`) and template sheet names
  (`MRP ativos`, `IT PR1`). Translating these would break the tooling.

## Skill Writing Standards

- SKILL.md must have YAML frontmatter with `name` and `description`
- Description should explain both what the skill does AND when to trigger it
- Include "When NOT to use" section pointing to sibling skills
- Keep SKILL.md under 500 lines; use bundled references for overflow
- Use imperative form in instructions
- Explain the "why" behind instructions rather than relying on MUST/NEVER

## Tech Stack (design-system plugin)

- Next.js (App Router)
- Tailwind CSS v4
- shadcn/ui
- TypeScript
