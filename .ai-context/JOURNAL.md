# Journal — python-project-template

> **Usage — Claude Code** : ce fichier trace l'avancement du projet session par session —
> ce qui a été fait et ce qu'il reste à faire. Contrairement à `CURRENT.md` (état du code
> au moment d'une review), ce journal suit les décisions, les documents créés et les étapes
> franchies. Ajoute une entrée en haut (sous ce bloc) à chaque session de travail
> significative. Ne supprime pas les entrées précédentes.
>
> Format d'une entrée :
>
> ## [YYYY-MM-DD] — <titre court de la session>
> ### Fait
> ### Reste à faire
> ### Références

---

## [2026-11-20] — Tâches invoke du template (étapes 1 à 3)

### Fait

- Plan aligner-taches-invoke — Étape 2 : `pyproject.toml` (commitizen, pre-commit, okflint, `version_files`, `packages.find`), `.pre-commit-config.yaml`, `okf-base.yaml`, `docs/{specs,plans}/.gitkeep`, `.github/workflows/ci.yml`, `.cruftignore` retiré, `cookiecutter.json` en 3.13, `hooks/post_gen_project.py` (JOURNAL.md, `pre-commit install`), `tests/test_{log,main}.py` ; reformatage ruff de `log/__init__.py`, `__main__.py`, `CONTRIBUTING.md`.
- Vérifié sur un projet généré avec le vrai hook : `inv ci` (81 tests, 100 % de couverture), `inv hooks`, `inv clean`, `inv okflint`, `inv release --dry-run` (après un commit `feat`), `cz bump` qui crée `CHANGELOG.md` et met `__version__` à jour. Décisions CHANGELOG et okflint actées dans la spec.
- Plan aligner-taches-invoke — Étape 3 : `{{cookiecutter.project_slug}}/CONTRIBUTING.md` (section Contrôles, section Git avec finish/release/clean/branches, `perf:`, `tasks/projet.py`, `gh`) et `README.md` (prérequis gh, 3.13 seul, structure, tableau des tâches, `skip`) ; projet généré : `inv ci` et `inv okflint` verts.
- `docs/specs/aligner-taches-invoke.md` et `docs/plans/aligner-taches-invoke.md` créés (6 étapes) ; décisions dans la spec.
- Plan aligner-taches-invoke — Étape 1 : `tasks/__init__.py` (hooks, clean, finish, release, delete_branch, clean_branches, okflint), `tasks/projet.py`, `tests/test_tasks_{clean,finish,release,branches}.py`, F403 ignoré dans `pyproject.toml`, `.clean` (avancé de l'étape 2) ; branche `feature/aligner-taches-invoke`.
- Vérifié sur un projet généré dans le scratchpad : 78 tests passent, ruff et mypy verts sur `tasks/` et `tests/`, `inv -l` correct, une tâche de `tasks/projet.py` est découverte.

### Reste à faire

- Exécuter `docs/plans/aligner-taches-invoke.md` — Étape 4 : commit et push du template (accord explicite requis avant le push).
- Étape 3 non commitée sur `feature/aligner-taches-invoke` (étapes 1 et 2 : `5daeccc`, `51da7f5`).

### Références

- [Spec](../docs/specs/aligner-taches-invoke.md)
- [Plan](../docs/plans/aligner-taches-invoke.md)
- `{{cookiecutter.project_slug}}/tasks/__init__.py`
