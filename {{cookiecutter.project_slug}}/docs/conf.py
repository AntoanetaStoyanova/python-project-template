"""Configuration Sphinx pour {{cookiecutter.project_name}}."""

project = "{{cookiecutter.project_name}}"
author = "{{cookiecutter.author}}"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

html_theme = "furo"
