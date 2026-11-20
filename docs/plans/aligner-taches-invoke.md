---
type: plan
statut: en cours
redige_le: 2026-11-20
---

# Plan — Aligner le template sur les tâches invoke de cartograph

*Rédigé le : 20 novembre 2026*
*Référence : [aligner-taches-invoke.md](../specs/aligner-taches-invoke.md)*

## Objectif

Le template génère un projet avec les tâches de workflow de cartograph (sans dbt ni DuckDB), puis veille est mis à jour avec `cruft update`.

## Prérequis

- Python 3.13 : lancer les commandes via `uv run --python 3.13` (le `python3` du shell est en 3.9).
- `gh` connecté (déjà le cas) ; `cruft` 2.16 installé.
- Travailler sur une branche `feature/aligner-taches-invoke` du template.

## Étape 1 — Tâches Git, nettoyage et okflint dans `tasks/`

- [x] Créer la branche `feature/aligner-taches-invoke` dans le template.
- [x] `{{cookiecutter.project_slug}}/tasks/__init__.py` : reprendre de `cartograph/tasks/__init__.py` les tâches `hooks`, `clean`, `finish`, `release`, `delete_branch`, `clean_branches`, `okflint` et leurs helpers (`_read_clean`, `_clean_targets`, `_check_pattern`, `_clean_match`, `_check_target`, `_bump`, `_next_version`, `_open_release_pr`, `_changelog_section`, `_archive_journal`, `_journal_to_log`, `_merged_pr`, `_delete_branch`, `_check_deletable`, `_bumps_version`, `_touches_code`, `_confirm_without_bump`, `_current_branch`, `_require_clean`).
- [x] Adapter : `lint` → `uv run pre-commit run --all-files` ; `CODE_PATHS = ("src/", "tasks/")` ; `PROTECTED_PATHS` sans `data/*` ; aucun appel à `dbt()` dans `finish` et `release` ; `ci` sans clean ; docstrings d'une ligne (y compris `_clean_targets`).
- [x] Supprimer `push_develop`, `push_main` et `docs_clean`.
- [x] Créer `tasks/projet.py` (docstring de module seule) ; terminer `tasks/__init__.py` par `from .projet import *`.
- [x] `pyproject.toml` : `[tool.ruff.lint.per-file-ignores] "tasks/__init__.py" = ["F403"]`.
- [x] Tests : `{{cookiecutter.project_slug}}/tests/test_tasks_{clean,finish,release,branches}.py`, repris de `cartograph/tests/` sans les références à dbt, en couvrant `_clean_match`, `_check_pattern`, `_bumps_version`, `_touches_code`, `_changelog_section`, `_journal_to_log`.

## Étape 2 — Config, dépendances, CI et hook de génération

- [x] `cookiecutter.json` : `"python_version": "3.13"`.
- [x] `{{cookiecutter.project_slug}}/pyproject.toml` : ajouter `pre-commit>=4.7.0`, `okflint==0.5.1`, `commitizen>=4.19.3` au groupe `dev` ; ajouter `[tool.commitizen]` (cz_customize, repris de cartograph).
- [x] Créer `.pre-commit-config.yaml` (pre-commit-hooks, ruff-check, ruff-format, commitizen), `default_install_hook_types: [pre-commit, commit-msg]`, sans sqlfluff.
- [x] Créer `.clean` : `**/__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.coverage`, `coverage.json`, `htmlcov/`, `docs/_build/`, `src/*.egg-info/`.
- [x] Créer `okf-base.yaml` avec `name: {{cookiecutter.project_slug}}`, et `docs/specs/.gitkeep`, `docs/plans/.gitkeep`.
- [x] Créer `.github/workflows/ci.yml` : `uv sync` sans `--locked`, `uv run inv ci`, `${{ }}` entre `{% raw %}` ; actions épinglées comme dans cartograph.
- [x] Supprimer `.cruftignore` du template (jamais lu par cruft).
- [x] `hooks/post_gen_project.py` : créer `.ai-context/JOURNAL.md` avec l'en-tête du gabarit écrit en dur dans le hook (pas de dépendance à `~`) ; lancer `uv run pre-commit install` après le commit initial, qui ne passe pas les hooks.
- [x] Tests : générer un projet (`cruft create` local ou `cookiecutter` sur le dossier, hors du dépôt), puis vérifier `inv -l`, `inv ci`, `inv hooks`, `inv clean`, `inv okflint`, `inv release --dry-run`. Trancher CHANGELOG.md et le comportement d'okflint sans documents ; ajuster le template en conséquence.
- [x] Ajouts nécessaires à `inv ci` d'un projet généré : `tests/test_log.py` et `tests/test_main.py` (couverture 100 % ≥ 88 %), `[tool.setuptools.packages.find]` corrigé (`where = ["src"]`, le paquet n'était pas importable), `version_files` commitizen sur `__version__`, reformatage de `log/__init__.py`, `__main__.py` et `CONTRIBUTING.md` pour ruff.

## Étape 3 — Documentation du template

- [x] `CONTRIBUTING.md` : section Contrôles (`inv ci`, `inv lint` via pre-commit) ; section Git (branches `feature/*`, `inv finish`, `inv release`, `inv clean`, `inv delete-branch`, `inv clean-branches`, `inv hooks`, `inv okflint`) ; ajouter `perf:` au tableau des commits ; documenter `tasks/projet.py` pour les tâches du projet ; prérequis `gh`.
- [x] `README.md` du template : prérequis `gh`, Python 3.13 seul, nouvelles tâches, structure (`.clean`, `okf-base.yaml`, `.pre-commit-config.yaml`, `.github/`, `tasks/projet.py`), et la règle « après `cruft create` ou avant la première mise à jour, ajouter `tasks/projet.py` à `skip` dans `.cruft.json` ».
- [x] Tests : `inv okflint` et markdown de la doc passent sur le projet généré.

## Étape 4 — Commit et push du template

- [ ] Relancer la génération d'un projet de test, puis `inv ci` sur celui-ci.
- [ ] Commits Conventional (`feat:`, `docs:`, `test:`) sur `feature/aligner-taches-invoke`.
- [ ] Après accord explicite : `git push -u origin HEAD`, PR vers la branche par défaut du template, fusion. `cruft update` lit GitHub : le commit doit y être avant l'étape 5.

## Étape 5 — Mise à jour de veille

- [x] Dans veille, avant `cruft update` : créer `tasks/projet.py` avec `run` et `dry_run` (déplacés depuis `tasks/__init__.py`) et ajouter `"skip": ["tasks/projet.py"]` à `.cruft.json`.
- [x] `cruft update` (lancé par toi, commité avec des marqueurs de conflit non résolus) ; résoudre les conflits de `tasks/__init__.py` (prendre la version du template), `pyproject.toml` (garder les dépendances d'exécution `anthropic`, `beartype`, `feedparser`, `pyyaml`, ajouter celles du template) et `.cruftignore` (supprimé).
- [x] `uv sync` ; `uv run inv -l` : `run` et `dry_run` présents.
- [x] Créer `docs/specs` et `docs/plans` s'ils n'ont pas d'équivalent ; vérifier que `okf-base.yaml` accepte les specs et plans existants (`veille-quotidienne.md`, frontmatter).
- [x] Tests : `uv run inv ci` passe.
- [ ] Commits sur `develop` de veille ; pas de push sans demande.

## Étape 6 — Vérifications dans veille

- [x] `inv hooks` installe pre-commit et commit-msg.
- [x] `inv clean` supprime les fichiers générés sans toucher `.env`, `.venv`, `docs/`.
- [x] `inv okflint` passe.
- [ ] `inv release --dry-run` passe sur `develop` (`cz bump --dry-run`).
- [ ] Noter dans le journal de veille le tag cruft appliqué.


## Étape 7 — Premier tag git (blocage de `inv release`)

- [x] `tasks/__init__.py` : `_require_tag` (arrêt clair sans tag) appelé par `release` ; `in_stream=False` sur les appels `cz` (`_bump`, `_next_version`) pour qu'une question de `cz` échoue au lieu de bloquer.
- [x] `hooks/post_gen_project.py` : tag annoté `v<version>` posé sur le commit initial.
- [x] Tests : `test_release_refuses_missing_tag` (avec et sans `--dry-run`).
- [x] Générer un projet de test : `git tag` contient `v0.1.0`, `inv release --dry-run` ne bloque pas, `inv ci` passe ; sans tag, `inv release` s'arrête avec le message d'erreur.

## Critères de fin

- [ ] `uv run inv ci` passe sur un projet généré et sur veille.
- [ ] Critères d'acceptation de la spec cochés.
- [ ] Statut de la spec et du plan passé à `fait`.
