"""Visit https://nox.thea.codes/en/stable/ to see what this is. 

To run every session:

$ nox

To run a single session

$ nox --session build_readme

"""

import subprocess
from pathlib import Path
from unittest import result

import nox


def install_dev_requirements(session):
    session.run(
        "pip", "install", "-r", str(Path("requirements") / "dev_requirements.txt")
    )


def install_requirements(session):
    session.run("pip", "install", "-r", str(Path("requirements") / "requirements.txt"))


@nox.session
def build_readme(session):
    """Installs the requirements, recreates the main README and pushes it to the main branch."""
    install_requirements(session)
    session.run("python", "build_library.py", "-l")
    # Check if the README.md has changed at all, otherwise
    # stop running git to avoid failing the workflow
    result = subprocess.run(
        ["git", "diff", "README.md"], capture_output=True, encoding="utf-8"
    ).stdout
    if result == "":
        print("README.md didn't changed, that's it.")
    else:
        session.run("git", "config", "user.name", "agus", external=True)
        session.run(
            "git", "config", "user.email", "agustin.piqueres@gmail.com", external=True
        )
        session.run("git", "add", "README.md", external=True)
        session.run("git", "commit", "-m", "autocommit from within nox", external=True)
        session.run("git", "push", "upstream", "main", external=True)


@nox.session(python=["3.8", "3.9", "3.10"])
def tests(session):
    install_dev_requirements(session)
    install_requirements(session)
    session.run("pytest", "tests")


@nox.session
def lint(session):
    install_dev_requirements(session)
    install_requirements(session)
    session.run("isort", "build_library.py")
    session.run("black", "--check", "build_library.py")
