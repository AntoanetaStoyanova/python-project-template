# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Auteur

{{cookiecutter.author}}

## Prérequis

- Python >= {{cookiecutter.python_version}}
- [uv](https://docs.astral.sh/uv/)
- [cruft](https://cruft.github.io/cruft/) — pour mettre à jour le template

## Installation

```bash
git clone https://github.com//{{cookiecutter.project_slug}}.git
cd {{cookiecutter.project_slug}}
uv sync
```

## Utilisation

```bash
uv run python -m {{cookiecutter.project_slug}}
```

## Mettre à jour depuis le template

```bash
cruft update
```
