# Contributing to {{cookiecutter.project_name}}

Standards de développement du projet. Ces règles s'appliquent à tout contributeur humain ou IA (Claude Code inclus).

---

## Type hints

Obligatoires partout — arguments, valeurs de retour, variables ambiguës.

```python
def process(data: list[str], limit: int = 10) -> dict[str, int]: ...
```

- `mypy --strict` doit passer sans erreur
- Pas de `Any` sauf cas justifié par un commentaire

---

## Docstrings

Obligatoires sur tous les modules, classes et fonctions publiques. Format NumPy, résumé sur la ligne qui suit les guillemets, types repris de la signature :

```python
def fetch(url: str, timeout: int = 30) -> bytes:
    """
    Télécharge le contenu d'une URL.

    Parameters
    ----------
    url : str
        URL cible.
    timeout : int
        Délai max en secondes.

    Returns
    -------
    bytes
        Contenu brut de la réponse.

    Raises
    ------
    ValueError
        Si l'URL est invalide.
    """
```

Classes : section `Attributes` au même format. Doctests : section `Examples`.

Fonctions privées (`_nom`) : docstring courte en une ligne suffit.

---

## Style & formatage

Outil unique : **Ruff** (formatage + lint).

```bash
uv run ruff format .   # formate
uv run ruff check .    # lint
```

- Longueur de ligne : 88 caractères
- Guillemets doubles
- Imports triés automatiquement (isort via Ruff)

---

## Tests

```bash
uv run pytest          # lance tous les tests + coverage
```

- Couverture minimale : **88%** (bloquant en CI)
- Les doctests comptent (`--doctest-modules` activé)
- Un test = un comportement précis, pas une fonction
- Nommage : `test_<comportement>.py`, fonctions `test_<ce_qui_est_verifie>()`

---

## Contrôles

Une fois après le clonage :

```bash
uv sync
uv run inv hooks       # installe les hooks pre-commit et commit-msg
```

À chaque `git commit`, pre-commit contrôle les fichiers du commit (`.pre-commit-config.yaml`) : fins de ligne LF, fin de fichier, espaces en fin de ligne, BOM, gros fichiers, casse des noms, validité YAML, JSON et TOML, `ruff check`, `ruff format`, et le format du message (commitizen).

- Si un contrôle corrige un fichier, le commit est refusé : relire la correction, `git add`, recommencer le commit.
- `git commit --no-verify` saute les contrôles pour un commit de travail ; ils restent dus avant la pull request.

Avant une pull request, depuis la branche `feature/…` :

```bash
uv run inv finish      # inv ci et inv okflint, push, puis pull request vers develop
```

`inv finish` exige la CLI `gh` ; il refuse une autre branche qu'une `feature/…` et un arbre de travail non propre. Si la pull request existe déjà, il affiche son lien. Si la branche modifie `src/` ou `tasks/` sans aucun commit `feat`, `fix`, `refactor` ou `perf` (seuls préfixes qui font monter la version), il affiche les commits et demande confirmation avant le push ; « n » ou Entrée arrête la tâche, le temps d'un `git commit --amend`. Les contrôles se lancent aussi seuls :

```bash
uv run inv ci          # pre-commit sur tous les fichiers, mypy, pytest
uv run inv okflint     # en-tête et liens des specs et plans de docs/
```

`uv run inv clean` supprime les fichiers générés déclarés dans `.clean`, à la racine : un motif glob par ligne, relatif à la racine, `/` final pour un dossier, `#` pour un commentaire. Pour nettoyer un nouveau fichier généré, ajouter son motif à `.clean` plutôt qu'écrire un `rm`. La tâche échoue sans rien supprimer si un motif touche un fichier suivi par Git, sort du dépôt ou atteint un chemin protégé (`.env`, `.venv/`, `.git/`, `docs/plans/`, `docs/specs/`). `inv finish` et `inv release` la lancent à la fin ; `inv ci` non, pour garder `htmlcov/` après un échec.

Sur GitHub, le workflow `CI` (`.github/workflows/ci.yml`) lance `uv run inv ci` sur chaque pull request vers `develop` et `main`.

Les specs et plans de `docs/specs/` et `docs/plans/` commencent par un en-tête vérifié par okflint (`okf-base.yaml`) :

```yaml
---
type: plan             # spec, plan, note ou reference
statut: en cours       # brouillon, en cours, fait ou abandonné
redige_le: 2026-10-30
lot: CI-00             # facultatif
---
```

Les tâches propres au projet vont dans `tasks/projet.py`, jamais dans `tasks/__init__.py` (géré par le template). Le premier `cruft update` d'un projet exige d'ajouter `"skip": ["tasks/projet.py"]` à `.cruft.json`.

---

## Organisation du code

```
src/{{cookiecutter.project_slug}}/
├── __main__.py     # uniquement : from . import main; main()
├── bin/            # modules métier (fonctions), importés en {{cookiecutter.project_slug}}.bin.<module>
├── config/         # constantes et paramètres
├── data/           # chargement / sauvegarde de données
├── log/            # configuration des logs (jamais print() en production)
└── notebook/       # utilitaires pour notebooks Jupyter
```

---

## Git

- Branches : `feature/<sujet>` (développement, créée depuis `develop`), `develop` (qualité), `main` (production, jamais modifiée en local)
- Cycle :
  1. `feature/…` se pousse librement et rejoint `develop` par une pull request, ouverte par `uv run inv finish` ;
  2. sur `develop` : `uv run inv release --dry-run` (version suivante et changelog, sans rien modifier), puis `uv run inv release` (pull, contrôles, archivage du journal, `cz bump`, documentation, push avec le tag, puis pull request `develop` → `main` titrée `Release vX.Y.Z`, avec la section de la version dans `CHANGELOG.md`) ;
  3. la pull request `develop` → `main` est fusionnée une fois le check `ci` vert.
- `inv release` archive dans `.ai-context/LOG.md` (une section par version) toutes les entrées de `.ai-context/JOURNAL.md` sauf la plus récente.
- Mettre une branche feature à jour après une release : `git fetch origin && git merge origin/develop`
- Fin de lot : `uv run inv clean-branches` liste les branches locales dont la pull request est fusionnée et, après confirmation (o/N), les supprime en local puis sur `origin`. Une seule branche : `uv run inv delete-branch <nom>`, refusée sans pull request fusionnée sauf `--force`. `main`, `develop` et la branche courante ne sont jamais supprimées, même avec `--force`.
- `gh` doit être installé et connecté (`gh auth login`) : `finish`, `release`, `delete-branch` et `clean-branches` l'utilisent.
- Format des commits — **Conventional Commits**, vérifié par le hook `commit-msg`. Chaque message devient une ligne du `CHANGELOG.md` : l'écrire pour être relu.

| Préfixe | Usage | Version (0.x) | Changelog |
|---------|-------|---------------|-----------|
| `feat:` | nouvelle fonctionnalité | mineure | Nouveautés |
| `fix:` | correction de bug | correctif | Corrections |
| `refactor:` | réécriture sans changement de comportement | correctif | Réécritures |
| `perf:` | performance | correctif | Performances |
| `docs:` | documentation uniquement | aucune | Documentation |
| `test:` | ajout ou correction de tests | aucune | Tests |
| `chore:` | maintenance, dépendances, config | aucune | Maintenance |

- `!` après le type (`feat!:`) marque un changement cassant : mineure tant que la version est en 0.x
- Une release ne contenant que `docs`, `test` ou `chore` ne crée pas de version ; ces commits partent dans la suivante
- `bump:` est réservé au commit créé par `inv release`

---

## Règles générales

- Commenter le **pourquoi**, jamais le **quoi** (le code doit se lire seul)
- Pas de code mort commenté — git conserve l'historique
- Pas de `print()` en production — passer par `log/`
- Pas de gestion d'erreurs pour des cas impossibles — ne pas sur-défendre le code
- Pas d'abstraction prématurée — trois lignes similaires valent mieux qu'une abstraction inutile
