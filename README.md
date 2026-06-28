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

Estes são **plugins do Claude Code** — funcionam em qualquer ambiente onde o Claude Code roda:
terminal (CLI), app desktop do Claude Code e extensões de IDE (VS Code / JetBrains). Em todos os
casos, primeiro adiciona-se o marketplace e depois instala-se cada plugin desejado.

Plugins disponíveis: `design-system`, `plugin-updater`, `marketing-campaigns`, `dev-workflows`.

### Terminal (CLI)

```bash
# 1. Adicionar o marketplace
/plugin marketplace add Rampap-Brasil/rampap-skills

# 2. Instalar um plugin (exemplo)
/plugin install design-system@Rampap-Brasil/rampap-skills
```

Comandos úteis: `/plugin marketplace list`, `/plugin marketplace update Rampap-Brasil/rampap-skills`.

### App Desktop do Claude Code (Mac/Windows)

1. Abra o Claude Code e vá para a aba **Code**.
2. Abra o gerenciador de plugins (botão **+** ao lado do prompt → **Plugins**).
3. Na aba **Marketplaces**, adicione: `Rampap-Brasil/rampap-skills`.
4. Na aba **Plugins**, instale os plugins desejados e escolha o escopo (você / projeto / local).

> Observação: plugins não ficam disponíveis em sessões na nuvem do app desktop (apenas em sessões locais e via SSH).

### Extensão do VS Code

1. Digite `/plugins` na caixa de prompt para abrir o gerenciador de plugins.
2. Na aba **Marketplaces**, adicione: `Rampap-Brasil/rampap-skills`.
3. Na aba **Plugins**, instale os plugins desejados.

### JetBrains (IntelliJ, PyCharm, etc.)

Use os mesmos comandos da CLI no terminal integrado da IDE:

```bash
/plugin marketplace add Rampap-Brasil/rampap-skills
/plugin install <nome-do-plugin>@Rampap-Brasil/rampap-skills
```

### Onde NÃO funciona

- **Claude Code na web** (claude.ai/code) — ambiente em nuvem, sem suporte a plugins/marketplaces.
- **App Claude Desktop comum** e **chat do claude.ai** — são produtos diferentes do Claude Code.
  Eles usam "Agent Skills" (carregadas via claude.ai/API), um sistema separado e **incompatível**
  com este marketplace de plugins do Claude Code.

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
