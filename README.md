# Rampap Skills

Marketplace de skills para o Claude Code — toolkit de design system e fluxos de trabalho de desenvolvimento da Rampap.

## Plugins

### design-system

Toolkit para construir e manter design systems com shadcn/ui, Tailwind CSS v4 e Next.js.

| Skill | Comando | Descrição |
|-------|---------|-----------|
| **setup** | `/design-system:setup` | Extrai design tokens de um screenshot/Figma e monta um design system completo (globals.css, styleguide, componentes de demonstração) |
| **add-component** | `/design-system:add-component` | Adiciona um componente do registro shadcn ou cria um customizado, com página de showcase e navegação no styleguide |
| **build-page** | `/design-system:build-page` | Constrói uma página completa a partir de um screenshot/Figma usando os componentes e tokens do design system existente |

**Fluxo de trabalho:**

```
1. design-system:setup          → Iniciar a partir de uma referência visual
2. design-system:add-component  → Adicionar componentes um a um
3. design-system:build-page     → Construir páginas a partir de designs
```

## Instalação

Adicione este marketplace ao Claude Code:

```bash
/plugins install github:Rampap-Brasil/rampap-skills
```

## Estrutura do repositório

```
rampap-skills/
├── .claude-plugin/
│   └── marketplace.json          # Registro do marketplace
├── plugins/
│   └── design-system/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Metadados do plugin
│       └── skills/
│           ├── setup/
│           ├── add-component/
│           └── build-page/
└── CLAUDE.md                     # Convenções do projeto
```

## Licença

MIT
