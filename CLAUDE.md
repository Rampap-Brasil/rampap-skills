# Rampap Skills — Project Conventions

## Repository Structure

```
rampap-skills/
├── .claude-plugin/
│   └── marketplace.json        # Marketplace registry — lists all plugins
├── plugins/
│   └── <plugin-name>/
│       ├── plugin.json          # Plugin metadata (name, version, author)
│       └── skills/
│           └── <skill-name>/
│               ├── SKILL.md     # Skill instructions (required)
│               └── ...          # Bundled resources (scripts/, references/, assets/)
├── CLAUDE.md                    # This file
└── README.md
```

## Adding a New Plugin

1. Create `plugins/<plugin-name>/plugin.json` with name, description, version, author
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
