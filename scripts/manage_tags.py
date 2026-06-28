#!/usr/bin/env python3
"""Gerencia as tags por-plugin do marketplace rampap-skills.

Deriva a tag `<plugin>-v<versao>` da versao declarada em cada
`plugins/<plugin>/.claude-plugin/plugin.json`, valida a consistencia com o
`.claude-plugin/marketplace.json` e cria as tags faltantes (idempotente).

A tag e criada apontando para o COMMIT onde a versao foi introduzida (o ultimo
commit que tocou aquele plugin.json) — e somente se esse bump ja estiver commitado.
Assim o hook Stop pode rodar em qualquer branch sem criar tags em commits errados.

Uso:
    python3 scripts/manage_tags.py            # valida + cria as tags faltantes (apply)
    python3 scripts/manage_tags.py --check    # valida + reporta; NAO cria nada

Convencao de tag: `<plugin>-v<versao>` (ex.: design-system-v1.0.1).

Codigo de saida:
    0  -> consistente (em --apply, tags criadas com sucesso)
    1  -> ha inconsistencia de versao entre plugin.json e marketplace.json
          (o pre-push usa isso para BLOQUEAR o push). Tags faltantes, sozinhas,
          NAO bloqueiam — apenas geram aviso.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True)


def repo_root() -> Path:
    r = run(["git", "rev-parse", "--show-toplevel"])
    if r.returncode != 0:
        print("Nao e um repositorio git — nada a fazer.")
        sys.exit(0)
    return Path(r.stdout.strip())


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def existing_tags() -> set[str]:
    r = run(["git", "tag", "--list"])
    return {t for t in r.stdout.splitlines() if t.strip()}


def last_commit_for(relpath: str) -> str | None:
    r = run(["git", "log", "-1", "--format=%H", "--", relpath])
    sha = r.stdout.strip()
    return sha or None


def version_at_commit(commit: str, relpath: str) -> str | None:
    r = run(["git", "show", f"{commit}:{relpath}"])
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout).get("version")
    except json.JSONDecodeError:
        return None


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    root = repo_root()

    # Versoes declaradas no marketplace.json (fonte que o usuario ve)
    market: dict[str, str] = {}
    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    if marketplace_path.exists():
        for entry in load_json(marketplace_path).get("plugins", []):
            market[entry.get("name")] = entry.get("version")

    # Versoes declaradas em cada plugin.json (working tree)
    plugins: dict[str, tuple[str, str]] = {}  # name -> (version, relpath)
    for pj in sorted(root.glob("plugins/*/.claude-plugin/plugin.json")):
        data = load_json(pj)
        plugins[data["name"]] = (data["version"], str(pj.relative_to(root)))

    if not plugins:
        print("Nenhum plugin encontrado em plugins/*/.claude-plugin/plugin.json.")
        return 0

    tags = existing_tags()
    problems: list[str] = []        # inconsistencias -> bloqueiam
    missing: list[str] = []         # tags faltantes prontas para criar (bump commitado)
    deferred: list[str] = []        # bump ainda nao commitado -> tag adiada
    created: list[str] = []

    for name, (version, relpath) in plugins.items():
        # 1) consistencia plugin.json x marketplace.json
        if name not in market:
            problems.append(f"plugin '{name}' (v{version}) nao esta registrado no marketplace.json")
        elif market[name] != version:
            problems.append(
                f"plugin '{name}': versao divergente — plugin.json={version} x marketplace.json={market[name]}"
            )

        tag = f"{name}-v{version}"
        if tag in tags:
            continue

        # 2) so podemos taguear se o bump ja estiver commitado
        commit = last_commit_for(relpath)
        if commit is None or version_at_commit(commit, relpath) != version:
            deferred.append(f"{tag} (versao ainda nao commitada — sera tagueada apos o commit)")
            continue

        if check_only or problems:
            missing.append(f"{tag} -> {commit[:9]}")
        else:
            r = run(["git", "tag", "-a", tag, commit, "-m", f"{name} {version}"])
            if r.returncode == 0:
                created.append(tag)
                print(f"Tag criada: {tag} ({commit[:9]})")
            else:
                problems.append(f"falha ao criar a tag {tag}: {r.stderr.strip()}")

    for name in market:
        if name not in plugins:
            problems.append(
                f"marketplace.json lista '{name}', mas nao ha plugins/{name}/.claude-plugin/plugin.json"
            )

    if problems:
        print("Inconsistencias de versao (corrija antes de taguear/publicar):")
        for p in problems:
            print(f"  - {p}")
    if missing:
        if check_only:
            print("Tags faltantes (rode `python3 scripts/manage_tags.py` para criar):")
        else:
            print("Tags faltantes nao criadas por causa das inconsistencias acima:")
        for m in missing:
            print(f"  - {m}")
    if deferred:
        print("Tags adiadas:")
        for d in deferred:
            print(f"  - {d}")

    if not problems and not missing and not deferred and not created:
        print("OK: todas as versoes sao consistentes e ja possuem tag.")
    if created:
        print(f"{len(created)} tag(s) criada(s). Publique com: git push --follow-tags")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
