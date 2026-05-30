"""Hook exécuté automatiquement après la génération du projet."""

import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path


PROJECT_SLUG = "{{cookiecutter.project_slug}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
    return subprocess.run(cmd, check=check)


def is_cruft_update() -> bool:
    """Vrai si le hook tourne dans un dossier temp — cas d'un cruft update."""
    return str(Path.cwd()).startswith(tempfile.gettempdir())


def main() -> None:
    # Pendant cruft update, le hook tourne dans un dossier temporaire.
    # On ne refait pas le setup (git init, uv, GitHub) — on laisse Cruft
    # appliquer seulement le diff de template.
    if is_cruft_update():
        return

    # 1. Injecter la date du jour dans CURRENT.md
    current_md = Path(".ai-context/CURRENT.md")
    current_md.write_text(
        current_md.read_text().replace("__INIT_DATE__", date.today().isoformat())
    )

    # 2. Initialiser git et créer la branche develop
    run(["git", "init"])
    run(["git", "checkout", "-b", "develop"])

    # 3. Vérifier que uv est installé
    if not shutil.which("uv"):
        print("\n[ERREUR] 'uv' n'est pas installé ou introuvable dans le PATH.")
        print("Installe-le via : https://docs.astral.sh/uv/getting-started/installation/")
        sys.exit(1)

    # 4. Épingler la version Python et synchroniser l'environnement
    run(["uv", "python", "pin", PYTHON_VERSION])
    run(["uv", "sync"])

    # 5. Commit initial
    run(["git", "add", "."])
    run(["git", "commit", "-m", "chore: initial project structure from cruft template"])

    # 6. Demander si on pousse sur GitHub
    answer = input("\nVeux-tu pousser le projet sur GitHub ? [o/n] ").strip().lower()

    if answer != "o":
        print("\nPas de push automatique. Pour le faire manuellement plus tard :")
        print(f"  git remote add origin https://github.com/<ton_username>/{PROJECT_SLUG}.git")
        print("  git push -u origin develop")
        print("\nNote : .cruft.json est déjà présent. 'cruft update' fonctionnera")
        print("dès que le remote GitHub sera configuré.")
    else:
        github_username = input("Ton GitHub username : ").strip()
        remote_url = f"https://github.com/{github_username}/{PROJECT_SLUG}.git"

        print(f"\nUtilisation des credentials Git déjà configurés sur ta machine.")
        print(f"(token HTTPS via 'gh auth login' ou clé SSH)")
        print(f"Remote : {remote_url}")

        run(["git", "remote", "add", "origin", remote_url])
        result = run(["git", "push", "-u", "origin", "develop"], check=False)

        if result.returncode != 0:
            print("\n[ERREUR] Le push a échoué.")
            print("Cause probable : le repo GitHub a été créé avec un README auto-généré.")
            print("Pour écraser ce contenu et pousser ton projet :")
            print()
            print(f"  git push --force-with-lease -u origin develop")
            print()
            print("Ou si tu préfères récupérer d'abord le contenu distant :")
            print()
            print(f"  git pull origin develop --allow-unrelated-histories")
            print(f"  git push -u origin develop")
        else:
            print(f"\nSucces ! Le projet '{PROJECT_SLUG}' est disponible sur GitHub.")
            print(f"  {remote_url.replace('.git', '')}")

    # 7. Récapitulatif final
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], text=True
    ).strip()

    print("\n" + "=" * 60)
    print(f"  Projet '{PROJECT_SLUG}' genere avec succes !")
    print("=" * 60)
    print(f"  Git branch active : {branch}")
    print()
    print("  Lance ces commandes pour demarrer :")
    print()
    print(f"    cd {PROJECT_SLUG}")
    print(f"    source .venv/bin/activate")
    print()
    print("  Ou en une ligne :")
    print()
    print(f"    cd {PROJECT_SLUG} && source .venv/bin/activate")
    print()
    print("  Mettre a jour le template plus tard : cruft update")
    print("=" * 60)


if __name__ == "__main__":
    main()
