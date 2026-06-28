#!/usr/bin/env bash
#
# Instala os hooks de gerenciamento de tags do rampap-skills.
#
#  1) Git hooks versionados (.githooks/): valida versoes/tags e bloqueia o push
#     em caso de inconsistencia. Vale para todo o time (enforcement).
#  2) Claude Code Stop hook (LOCAL, por desenvolvedor): cria as tags faltantes
#     automaticamente durante o trabalho via Claude Code. Fica em .claude/settings.json,
#     que e ignorado pelo git — portanto e opcional e nao afeta os colegas.
#
# Rode uma vez por clone:  bash scripts/install-hooks.sh
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"

# 1) Git hooks versionados
git config core.hooksPath .githooks
git config push.followTags true
chmod +x .githooks/* scripts/*.sh scripts/*.py 2>/dev/null || true
echo "Git hooks instalados: core.hooksPath=.githooks, push.followTags=true"

# 2) Claude Code Stop hook (local, opcional)
settings=".claude/settings.json"
mkdir -p .claude
python3 - "$root" "$settings" <<'PY'
import json, os, sys
root, settings = sys.argv[1], sys.argv[2]
cmd = f'bash "{root}/scripts/stop_hook_tags.sh"'
data = {}
if os.path.exists(settings):
    with open(settings, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
stop = data.setdefault("hooks", {}).setdefault("Stop", [])
exists = any(h.get("command") == cmd for grp in stop for h in grp.get("hooks", []))
if exists:
    print(f"Claude Code Stop hook ja presente em {settings} — nada a fazer.")
else:
    stop.append({"hooks": [{"type": "command", "command": cmd}]})
    with open(settings, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Claude Code Stop hook adicionado em {settings} (local, nao versionado).")
PY

echo ""
echo "Pronto. O Stop hook entra em vigor apos abrir /hooks ou reiniciar a sessao do Claude Code."
echo "Para criar tags faltantes manualmente a qualquer momento: python3 scripts/manage_tags.py"
