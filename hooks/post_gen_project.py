"""Hook exécuté automatiquement après la génération du projet."""

import shutil
import subprocess
import sys


PROJECT_SLUG = "{{cookiecutter.project_slug}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
    return subprocess.run(cmd, check=check)


def main() -> None:
    # 1. Initialiser git et créer la branche develop
    run(["git", "init"])
    run(["git", "checkout", "-b", "develop"])

    # 2. Vérifier que uv est installé
    if not shutil.which("uv"):
        print("\n[ERREUR] 'uv' n'est pas installé ou introuvable dans le PATH.")
        print("Installe-le via : https://docs.astral.sh/uv/getting-started/installation/")
        sys.exit(1)

    # 3. Épingler la version Python et synchroniser l'environnement
    run(["uv", "python", "pin", PYTHON_VERSION])
    run(["uv", "sync"])

    # 4. Commit initial
    run(["git", "add", "."])
    run(["git", "commit", "-m", "chore: initial project structure from cruft template"])

    # 5. Demander si on pousse sur GitHub
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
            print("\n[ERREUR] Le push a échoué. Commandes manuelles :")
            print(f"  git remote set-url origin {remote_url}")
            print("  git push -u origin develop")
        else:
            print(f"\nSucces ! Le projet '{PROJECT_SLUG}' est disponible sur GitHub.")
            print(f"  {remote_url.replace('.git', '')}")

    # 6. Récapitulatif final
    print("\n" + "=" * 60)
    print(f"Projet '{PROJECT_SLUG}' genere avec succes !")
    print("=" * 60)
    print(f"  Branche active        : develop")
    print(f"  Activer l'environnement : source .venv/bin/activate")
    print(f"  Mettre a jour le template : cruft update")
    print("=" * 60)


if __name__ == "__main__":
    main()
