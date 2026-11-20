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

## [2026-11-20] — Tâches invoke du template (étape 1)

### Fait

- `docs/specs/aligner-taches-invoke.md` et `docs/plans/aligner-taches-invoke.md` créés (6 étapes) ; décisions dans la spec.
- Plan aligner-taches-invoke — Étape 1 : `tasks/__init__.py` (hooks, clean, finish, release, delete_branch, clean_branches, okflint), `tasks/projet.py`, `tests/test_tasks_{clean,finish,release,branches}.py`, F403 ignoré dans `pyproject.toml`, `.clean` (avancé de l'étape 2) ; branche `feature/aligner-taches-invoke`.
- Vérifié sur un projet généré dans le scratchpad : 78 tests passent, ruff et mypy verts sur `tasks/` et `tests/`, `inv -l` correct, une tâche de `tasks/projet.py` est découverte.

### Reste à faire

- Exécuter `docs/plans/aligner-taches-invoke.md` — Étape 2 : config, dépendances, CI et hook de génération (`.pre-commit-config.yaml`, `okf-base.yaml`, `ci.yml`, commitizen, `python_version`).
- Étape 2 : `inv lint` échoue sur un projet généré tant que `log/__init__.py` (E501) et les blocs Python de `CONTRIBUTING.md` ne sont pas reformatés par ruff.
- Non commité : aucun commit sur `feature/aligner-taches-invoke`.

### Références

- [Spec](../docs/specs/aligner-taches-invoke.md)
- [Plan](../docs/plans/aligner-taches-invoke.md)
- `{{cookiecutter.project_slug}}/tasks/__init__.py`
