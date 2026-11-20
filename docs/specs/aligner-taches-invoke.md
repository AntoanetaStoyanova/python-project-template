---
type: spec
statut: en cours
redige_le: 2026-11-20
---

# Spec — Aligner le template sur les tâches invoke de cartograph

*Rédigé le : 20 novembre 2026*

## Contexte

Cartograph (`cartograph/tasks/__init__.py`, 576 lignes) a des tâches de workflow Git que le template n'a pas : hooks, clean, finish, release, gestion des branches, okflint. Le template n'a que lint, fmt, typecheck, check, test, ci, docs, docs_clean, push_develop et push_main. Veille est créé depuis le template au commit `612f699` et doit récupérer ces tâches par `cruft update`.

## Objectif

Le template génère un projet qui a, hors dbt et DuckDB, les mêmes tâches, la même config et la même doc que cartograph. Veille est mis à jour avec `cruft update`, et ses tâches `run` et `dry_run` survivent aux mises à jour suivantes.

## Périmètre

- Template : `tasks/__init__.py`, `tasks/projet.py`, `pyproject.toml`, `.pre-commit-config.yaml`, `.clean`, `okf-base.yaml`, `.github/workflows/ci.yml`, `CONTRIBUTING.md`, `cookiecutter.json`, `hooks/post_gen_project.py`, `README.md`.
- Tests pytest des tâches, repris de `cartograph/tests/test_tasks_{clean,finish,release,branches}.py` et adaptés.
- Veille : `cruft update`, résolution des conflits, `uv sync`, `inv ci`, vérification de `hooks`, `clean`, `okflint`, `release --dry-run`.

## Hors périmètre

- Tâches de cartograph propres au projet : dbt, sql_fmt, couverture_tests, regles, collect, rebuild, suivi, et les constantes DATABASE, SAMPLE_*, REAL_DATA_TAG.
- Hooks pre-commit markdownlint, prettier, actionlint, zizmor, sqlfluff.
- `beartype` et `beartype_this_package()` : absents du template aujourd'hui, à traiter dans un plan à part.
- Toucher à cartograph.

## Décisions

| Sujet | Décision | Raison |
|-------|----------|--------|
| Version Python | `cookiecutter.json` : `python_version` devient `"3.13"` (plus de liste) | `PurePosixPath.full_match` (`_clean_match`) exige 3.13 ; les choix 3.10 à 3.12 casseraient `inv clean`. Veille est déjà en 3.13, son contexte cruft ne change pas. |
| Tâches propres au projet | Le template possède `tasks/__init__.py` ; chaque projet met les siennes dans `tasks/projet.py`, que `__init__` importe par `from .projet import *` | Un fichier de projet que cruft ne touche plus évite le conflit sur `tasks/__init__.py` à chaque mise à jour. |
| Exclusion de `tasks/projet.py` | Le template livre un `tasks/projet.py` vide ; chaque projet l'ajoute à `skip` dans son `.cruft.json` | `skip` est la seule clé que cruft lit. `.cruftignore` n'est lu par aucune version de cruft : le fichier est retiré du template. |
| F403 sur le star import | `[tool.ruff.lint.per-file-ignores] "tasks/__init__.py" = ["F403"]` dans `pyproject.toml` | Évite un commentaire `noqa`. |
| JOURNAL.md | Créé par le hook post-génération (en-tête écrit en dur dans le hook), non livré comme fichier du template | Chaque projet le réécrit tous les jours ; un fichier du template entrerait en conflit à chaque `cruft update`. Veille a déjà le sien. |
| LOG.md | Non livré | `_archive_journal` le crée au premier `inv release`. |
| CHANGELOG.md | Non livré | Vérifié : `cz bump --yes` le crée au premier bump. |
| okflint sans specs ni plans | Le template livre `docs/specs/.gitkeep` et `docs/plans/.gitkeep` | Vérifié : `inv okflint` passe sans document. Ces dossiers sont dans `PROTECTED_PATHS`. |
| Config pre-commit | `pre-commit-hooks` (yaml, toml, json, fins de ligne, espaces), ruff-check, ruff-format, commitizen (commit-msg) | Demande « ruff, fichiers ». markdownlint, prettier, actionlint et zizmor demandent Node et ne sont pas demandés. |
| `docs_clean` | Supprimée | Cartograph l'a retirée, `docs/_build/` est dans `.clean`. |
| `PROTECTED_PATHS` | `.env`, `.venv`, `.git`, `docs/plans`, `docs/specs` | Les chemins `data/*` de cartograph n'existent pas dans le template. |
| `CODE_PATHS` | `("src/", "tasks/")` | Demande. |
| Docstrings | Une ligne pour tous les helpers, y compris `_clean_targets` | Standard global et `CONTRIBUTING.md` du template : docstring courte pour les fonctions privées. |
| `ci` | `check` + `test` : ni clean, ni okflint | Demande ; okflint tourne dans `finish`. |
| `ci.yml` | `uv sync` sans `--locked`, `cache-dependency-glob: pyproject.toml`, `${{ }}` entre `{% raw %}` | `uv.lock` n'est pas versionné (commit `612f699`). |
| Version dans le code | `[tool.commitizen] version_files` met aussi à jour `__version__` de `__init__.py` | Sans cela `__version__` reste à 0.1.0 après `cz bump`. |
| Paquet importable | `packages.find` : `where = ["src"]`, `include = ["<slug>*"]` | Le template installait un paquet `src` ; les tests importaient `<slug>` sans succès. |
| `gh` | Prérequis documenté dans `README.md` et `CONTRIBUTING.md` | `finish`, `release`, `delete_branch` et `clean_branches` l'utilisent. |

## Critères d'acceptation

- [ ] `inv -l` d'un projet généré liste hooks, clean, finish, release, delete-branch, clean-branches, okflint et ne liste ni push-develop, push-main, docs-clean, dbt.
- [ ] `inv lint` lance `pre-commit run --all-files`.
- [ ] `inv ci` passe sur un projet généré et n'appelle ni clean ni okflint.
- [ ] `inv clean` refuse un motif qui touche un chemin protégé ou un fichier suivi par Git.
- [ ] `inv release --dry-run` passe sur `develop` d'un projet généré.
- [ ] Les tests des helpers `_clean_match`, `_check_pattern`, `_bumps_version`, `_touches_code`, `_changelog_section`, `_journal_to_log` passent.
- [ ] Une tâche ajoutée dans `tasks/projet.py` apparaît dans `inv -l`.
- [ ] Veille : `cruft update` appliqué, `run` et `dry_run` conservés, `inv ci`, `inv hooks`, `inv clean`, `inv okflint` et `inv release --dry-run` passent.
