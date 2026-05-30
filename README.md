# python-project-template

Template Cruft pour créer des projets Python structurés et prêts à développer.

Chaque projet généré inclut : environnement uv, linting Ruff, typage mypy strict, tests pytest avec coverage, standards de contribution et suivi d'état pour Claude Code.

---

## Prérequis

| Outil | Rôle | Installation |
|-------|------|-------------|
| [**uv**](https://docs.astral.sh/uv/) | Gestion de l'environnement Python et des dépendances | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [**cruft**](https://cruft.github.io/cruft/) | Génération de projet et mises à jour depuis le template | `uv tool install cruft` |

---

## Créer un nouveau projet

```bash
cruft create https://github.com/AntoanetaStoyanova/python-project-template
```

Cruft pose ces questions :

| Question | Variable | Exemple |
|----------|----------|---------|
| Nom du projet | `project_name` | `My Data Pipeline` |
| Slug (auto-calculé) | `project_slug` | `my_data_pipeline` |
| Auteur | `author` | `Antoaneta Stoyanova` |
| Description | `description` | `Pipeline d'ingestion de données` |
| Version Python | `python_version` | `3.13` (choix dans liste) |

Le hook post-génération s'exécute automatiquement et :

1. Initialise git sur la branche `develop`
2. Épingle la version Python choisie avec `uv python pin`
3. Crée le virtualenv et installe les dépendances avec `uv sync`
4. Crée le commit initial
5. Propose de pousser le projet sur GitHub

---

## Structure du projet généré

```
mon_projet/
├── .ai-context/
│   └── CURRENT.md          # suivi d'état pour Claude Code (review datées)
├── src/mon_projet/
│   ├── __init__.py
│   ├── __main__.py
│   ├── bin/                # scripts d'entrée CLI
│   ├── config/             # constantes et paramètres
│   ├── data/               # chargement / sauvegarde
│   ├── log/                # configuration des logs
│   └── notebook/           # utilitaires Jupyter
├── tests/
├── CONTRIBUTING.md         # standards de développement Python
├── pyproject.toml          # ruff, mypy, pytest, coverage configurés
└── .gitignore
```

---

## Mettre à jour un projet existant

Quand ce template évolue, tous les projets générés peuvent récupérer les changements :

```bash
cd mon_projet
cruft update
```

Cruft compare le commit du template utilisé à la génération (tracé dans `.cruft.json`) avec le dernier commit sur `main` et propose un diff à appliquer.

---

## Ce qui est configuré dans chaque projet généré

| Outil | Config |
|-------|--------|
| **Ruff** | lint + format, ligne 88 chars, règles E/W/F/I/B/C4/UP |
| **mypy** | mode strict, `ignore_missing_imports = true` |
| **pytest** | doctests activés, coverage HTML + terminal |
| **coverage** | seuil minimum 88%, rapport des lignes manquantes |

---

## Développement du template

Pour modifier le template et propager les changements :

```bash
# 1. Modifier les fichiers dans {{cookiecutter.project_slug}}/ ou hooks/
# 2. Committer et pousser sur main
git add .
git commit -m "feat: ..."
git push origin main

# 3. Dans chaque projet généré, récupérer les changements
cruft update
```
