# Rampap Skills

Skills marketplace for Claude Code — design system toolkit and development workflows by Rampap.

## Plugins

### design-system

Toolkit for building and maintaining design systems with shadcn/ui, Tailwind CSS v4, and Next.js.

| Skill | Command | Description |
|-------|---------|-------------|
| **setup** | `/design-system:setup` | Extract design tokens from a screenshot/Figma and scaffold a complete design system (globals.css, styleguide, demo components) |
| **add-component** | `/design-system:add-component` | Add a component from shadcn registry or build custom, with showcase page and styleguide navigation |
| **build-page** | `/design-system:build-page` | Build a full page from a screenshot/Figma using existing design system components and tokens |

**Workflow:**

```
1. design-system:setup          → Bootstrap from visual reference
2. design-system:add-component  → Add components one by one
3. design-system:build-page     → Build pages from designs
```

## Installation

Add this marketplace to Claude Code:

```
/install-plugin rampap-skills
```

## Repository Structure

```
rampap-skills/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace registry
├── plugins/
│   └── design-system/
│       ├── plugin.json           # Plugin metadata
│       └── skills/
│           ├── setup/
│           ├── add-component/
│           └── build-page/
└── CLAUDE.md                     # Project conventions
```

## License

MIT
