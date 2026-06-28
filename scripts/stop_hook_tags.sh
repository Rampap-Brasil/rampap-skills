#!/usr/bin/env bash
#
# Wrapper do Claude Code Stop hook (LOCAL, por desenvolvedor).
# Cria as tags por-plugin faltantes de forma NAO-bloqueante. Se criar alguma,
# devolve um systemMessage informativo ao Claude Code; caso contrario, fica em
# silencio. Sempre sai com codigo 0 (nunca bloqueia o Stop).
#
# Instalado no .claude/settings.json local via scripts/install-hooks.sh.

root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[ -n "$root" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

out="$(cd "$root" && python3 scripts/manage_tags.py 2>&1)"

if printf '%s' "$out" | grep -q '^Tag criada:'; then
  msg="$(printf '%s' "$out" | grep '^Tag criada:' | tr '\n' ' ' | sed 's/\\/\\\\/g; s/"/\\"/g')"
  printf '{"systemMessage":"[manage-tags] %s"}\n' "$msg"
fi

exit 0
