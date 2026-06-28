# Changelog

Todas as mudanças relevantes do marketplace **Rampap Skills** são documentadas neste arquivo.

Este é um monorepo: cada plugin é versionado de forma independente, então as mudanças são
agrupadas por plugin. O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e as versões seguem o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

> Convenções: `Adicionado` = novos recursos, `Alterado` = mudanças em comportamento existente,
> `Corrigido` = correções de bug, `Removido` = recursos removidos.

---

## design-system

### [1.0.1] — 2026-02-25
#### Alterado
- Bump de manutenção após a reorganização do repositório para suporte a múltiplos plugins.

#### Corrigido
- Movido o `plugin.json` para `.claude-plugin/` e atualizado o comando de instalação.

### [1.0.0] — 2026-02-25
#### Adicionado
- Plugin `design-system` inicial com as skills `setup`, `add-component` e `build-page`
  (setup a partir de uma referência visual, adicionar componentes shadcn/customizados, construir
  páginas a partir de screenshots/Figma).
- Primeira versão do marketplace `rampap-skills`.

---

## plugin-updater

### [1.1.0] — 2026-02-25
#### Alterado
- Melhoria na skill `update-plugins` com compatibilidade com Windows e um pull explícito do
  marketplace antes de atualizar.

### [1.0.0] — 2026-02-25
#### Adicionado
- Plugin inicial (originalmente chamado `plugin-manager`) com as skills `update-plugins` e
  `update-skills`.
#### Alterado
- Renomeado o plugin de `plugin-manager` para `plugin-updater`.

---

## marketing-campaigns

### [0.2.0] — 2026-06-28
#### Adicionado
- Flag `--lang` no `etl_mrp.py`: os logs de execução são emitidos na língua preferencial do
  usuário (padrão `pt-BR`, fallback em inglês).
#### Alterado
- Prompts do agente (corpo do SKILL.md, `description` e arquivos em `references/`) padronizados em
  inglês, mantendo os identificadores de dados externos (nomes de colunas do MRP/Sankhya, nomes
  de abas do template) verbatim.
#### Corrigido
- Corrigidas as anotações de tipo `str | None` que falhavam no Python 3.9
  (`from __future__ import annotations`).

### [0.1.0] — 2026-03-29
#### Adicionado
- Plugin `marketing-campaigns` inicial com a skill `etl`: transforma o export bruto do MRP do
  Sankhya no template de Campanhas PRs da Rampap, filtrando produtos inativos e em ruptura.

---

## dev-workflows

### [1.0.1] — 2026-06-28
#### Alterado
- Skill `clean-session-branches` com prompt do agente padronizado em inglês; as instruções de
  output agora seguem dinamicamente a língua preferencial do usuário (em vez de pt-BR fixo).

### [1.0.0] — 2026-06-28
#### Adicionado
- Plugin `dev-workflows` inicial com a skill `clean-session-branches`: limpeza local de branches
  git em duas fases (auto-limpeza segura das branches da sessão já mergeadas em `develop`, mais
  sanitização opt-in das demais branches mergeadas).

---

## tlc-spec-driven

### [1.0.0] — 2026-06-28
#### Adicionado
- Plugin `tlc-spec-driven` inicial: skill-shim que carrega o conteúdo canônico da skill
  `tlc-spec-driven` (Tech Lead's Club, v3.1.0) via MCP `agent-skills`, **sem vendorizar** os
  arquivos de referência — evitando desatualização. A `description` espelha a canônica para
  preservar o auto-trigger.
- `.mcp.json` embarcado na raiz do plugin, que registra o servidor `agent-skills`
  automaticamente ao instalar/habilitar o plugin (contorna o bug upstream do arquivo `mcp.json`
  sem ponto no plugin `agent-skills-mcp`).
- Skill `setup` idempotente: detecta o estado atual e, como fallback, registra o MCP em escopo
  user (`claude mcp add ... --scope user`), com verificação real via `claude mcp list`
  (`✔ Connected`).
