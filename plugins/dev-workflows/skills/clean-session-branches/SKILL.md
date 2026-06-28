---
name: clean-session-branches
description: Use when the user wants to clean up local git branches after merging work into develop — deletes branches created during this conversation that are already merged into develop, then offers the remaining merged branches for explicit, opt-in deletion. Local branches only; never touches protected/long-lived branches (main, master, develop, sandbox, staging, homolog, production, qa) or the current branch.
---

# Limpeza de branches da sessão

Limpa branches **locais** em duas fases: automação segura para o que eu mesmo criei nesta
conversa e já está mergeado, e sanitização opt-in para o restante. Nunca usa `git branch -D`
(force) — sempre `git branch -d`, que recusa deletar trabalho não mergeado.

## Quando NÃO usar

- Para remover branches **remotas** ou podar `refs/remotes/*` — esta skill é deliberadamente
  *local-only*. Use `git push origin --delete <branch>` / `git remote prune origin` manualmente.
- Para deletar branches **não mergeadas** ou forçar deleção (`git branch -D`) — esta skill nunca
  força; trabalho não publicado é preservado por design.

## Pré-condições

1. Confirme que está num repositório git: `git rev-parse --is-inside-work-tree`.
2. Confirme que a branch `develop` existe: `git rev-parse --verify develop`. Se não existir,
   pergunte ao usuário qual é a branch base antes de continuar.

## Guard-rails (valem para as duas fases)

- **Branches protegidas — NUNCA delete**, em nenhuma das fases, mesmo que apareçam como
  mergeadas. A lista (case-insensitive) é:
  - a branch base (`develop` ou a informada nas pré-condições) e `main`/`master`;
  - branches de ambiente/longa duração: `sandbox`, `staging`, `homolog`, `homologacao`,
    `production`, `prod`, `qa`;
  - a branch atualmente em checkout (`git branch --show-current`).
- **Nunca** force a deleção. Opere **só em branches locais** — não toque em remotos nem em
  `refs/remotes/*`.
- Use sempre `git branch -d <nome>` (delete seguro). Se o git recusar (não mergeada, ou
  mergeada no HEAD mas à frente do próprio upstream), **não** force — reporte e siga em frente.

## Fase 1 — Auto-limpeza (sem confirmação)

1. **Monte a lista de candidatas da sessão.** Releia ESTA conversa e identifique as branches que
   **eu (Claude) criei** nela, procurando comandos que rodei do tipo `git checkout -b <nome>`,
   `git switch -c <nome>` e `git branch <nome>`. Essa é a lista `criadas_na_sessao`.
2. **Cruze com as mergeadas.** Rode `git branch --merged develop --format='%(refname:short)'`.
   As candidatas são `criadas_na_sessao ∩ merged`.
3. **Resolva a branch atual.** Se a branch em checkout estiver entre as candidatas, rode
   `git switch develop` antes de deletar (e remova-a/guard-rails da lista conforme acima).
4. **Delete** cada candidata com `git branch -d <nome>`.
5. **Reporte** em pt-BR: quais foram deletadas e quais foram puladas (com o motivo, ex.: "git
   recusou — não está totalmente mergeada").

## Fase 2 — Sanitização (escolha explícita do usuário)

6. **Calcule o restante.** Pegue `git branch --merged develop --format='%(refname:short)'` e
   remova: as deletadas na Fase 1, todas as **branches protegidas** (ver Guard-rails) e qualquer
   coisa que já tenha sido coberta.
7. Se **não sobrar nada**, informe que não há mais nada a sanitizar e encerre.
8. Se sobrar, **liste** cada branch restante com metadados úteis para a decisão. Sugestão de
   coleta por branch:
   - última data de commit: `git log -1 --format='%ci' <nome>`
   - autor do último commit: `git log -1 --format='%an' <nome>`
9. **Pergunte ao usuário** quais dessas deseja deletar. Default é **nenhuma** — não delete nada
   da Fase 2 sem escolha explícita.
10. **Delete** as escolhidas com `git branch -d <nome>` e **reporte** o resultado em pt-BR.

## Encerramento

Se a Fase 1 e a Fase 2 não tiverem nada a fazer, reporte "Nada a limpar." e encerre.

## Observações

- `git branch --merged` só detecta merges que preservam histórico (merge commit ou fast-forward).
  Com *squash/rebase merge* a branch não aparece como mergeada — por segurança, a skill
  (corretamente) não a deletará.
- Se a conversa for muito longa e o contexto tiver sido compactado, posso não enxergar branches
  criadas bem no início; elas simplesmente reaparecem na Fase 2 para escolha do usuário, em vez de
  serem perdidas.
- **Mergeada no HEAD mas à frente do upstream:** o `git branch -d` recusa deletar uma branch que
  está mergeada no `develop` mas tem commits locais ainda não enviados ao seu `origin/<branch>`
  (mensagem "not yet merged to refs/remotes/origin/..."). É comportamento esperado — reporte como
  pulada (commits locais não publicados) e **não** force; o usuário pode resolver manualmente.
- **Branch em uso por outro worktree:** o `git branch -d` também recusa deletar uma branch que está
  em checkout em outro worktree. Reporte como pulada (em uso em `<caminho>`) e siga em frente.
