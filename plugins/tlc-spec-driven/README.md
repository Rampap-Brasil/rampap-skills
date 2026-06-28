# tlc-spec-driven (shim)

Skill-shim que disponibiliza a skill **`tlc-spec-driven`** do [Tech Lead's Club](https://github.com/tech-leads-club/agent-skills)
dentro do Claude Code, **sem vendorizar** os arquivos da skill.

## O que é um shim e por quê

A `tlc-spec-driven` **não** é um plugin nativo do Claude Code: o conteúdo canônico (atualmente
v3.1.0, com ~11 arquivos de referência) vive num catálogo remoto, servido por um servidor MCP
(`agent-skills`) em fluxo de *progressive disclosure* (`search_skills` → `read_skill` →
`fetch_skill_files`). O MCP sempre entrega a versão mais recente.

Historicamente, copiavam-se os arquivos da skill para dentro de cada projeto (`.claude/skills`,
`.cursor/skills`, `.windsurf/skills`). Isso **desatualiza**: ao atualizar o catálogo, as cópias
vendorizadas ficavam presas numa versão antiga e a sombreavam (cópia local tem precedência).

A solução é este **shim**: um único `SKILL.md` minúsculo, visível como skill/slash, cujo corpo
apenas manda o agente carregar o conteúdo real via MCP. **Zero staleness**, sem versionar
arquivos de referência. A `description` espelha a canônica para preservar o auto-trigger por
linguagem natural.

## Como funciona

1. Você invoca a skill `tlc-spec-driven` (ou ela dispara sozinha pela `description`).
2. O shim garante que o MCP `agent-skills` esteja conectado (bootstrap).
3. Carrega o `SKILL.md` canônico via `read_skill` e as referências sob demanda via
   `fetch_skill_files`.
4. Segue as instruções aplicando o seu pedido.

## A dependência: o MCP `agent-skills`

Este plugin embarca um arquivo **`.mcp.json`** (na raiz do plugin) que declara o servidor
`agent-skills`. Ao instalar/habilitar o plugin, o Claude Code registra o servidor
**automaticamente** — basta um `/reload-plugins` (ou reiniciar a sessão) para as tools entrarem
no contexto.

### Bug upstream (por isso o `.mcp.json` é embarcado aqui)

O plugin `agent-skills-mcp` do marketplace `tech-leads-club` foi empacotado com o arquivo de
config nomeado `mcp.json` (**sem ponto**). O Claude Code só descobre MCP de plugin via
`.mcp.json` (**com ponto**) — então o servidor **nunca conectava** apenas instalando aquele
plugin. Este plugin contorna o problema embarcando o arquivo com o nome correto.

> Status do report upstream: a corrigir/registrar em `tech-leads-club/agent-skills`. Quando o
> upstream corrigir o nome do arquivo, este wrapper pode se tornar opcional.

### Setup de fallback

Se, mesmo após o reload, o servidor não subir, rode a skill **`tlc-spec-driven:setup`**. Ela é
**idempotente** (detecta se já está conectado e não faz nada nesse caso) e, como fallback,
registra o MCP em escopo de usuário:

```bash
claude mcp add agent-skills --scope user -- npx -y @tech-leads-club/agent-skills-mcp@latest
```

A skill confirma a mudança de config com você antes de gravar, e só se declara "ok" após
`claude mcp list` mostrar `✔ Connected`.

## Instalação

Veja o [README do marketplace](../../README.md) para adicionar o `rampap-skills`. Depois:

```bash
/plugin install tlc-spec-driven@Rampap-Brasil/rampap-skills
# em seguida, ative o MCP embarcado:
/reload-plugins
```

## Verificar

```bash
claude mcp list   # deve mostrar: agent-skills: ... ✔ Connected
```

## Desinstalar

- Registro de fallback (escopo user): `claude mcp remove agent-skills --scope user`
- Servidor embarcado pelo plugin: desinstale o plugin (`/plugin uninstall tlc-spec-driven@...`).

## Notas

- **`@latest` é proposital**: o catálogo entrega sempre a versão mais nova. Se você precisar de
  reprodutibilidade, pode pinar a versão do pacote MCP no `.mcp.json` (ex.: trocar `@latest` por
  `@0.1.3`) — ao custo de não receber atualizações automáticas.
- **Node**: o pacote pede `node >=24`; em Node 20/22 emite só o warning `EBADENGINE` e funciona
  mesmo assim.
- **Atribuição**: a skill canônica é de Felipe Rodrigues (github.com/felipfr), licença
  CC-BY-4.0. Este plugin é apenas um ponteiro para o conteúdo dele.
