"""Visit https://nox.thea.codes/en/stable/ to see what this is. 

To run every session:

$ nox

To run a single session

$ nox --session build_readme

"""

import nox
from pathlib import Path


def install_dev_requirements(session):
    session.run("pip", "install", "-r", str(Path("requirements") / "dev_requirements.txt"))


def install_requirements(session):
    session.run("pip", "install", "-r", str(Path("requirements") / "requirements.txt"))


@nox.session
def build_readme(session):
    """Installs the requirements, recreates the main README and pushes it to the main branch. """
    install_requirements(session)
    session.run("python", "build_library.py", "-l")
    session.run("git", "config", "user.name", "agus", external=True)
    session.run("git", "config", "user.email", "agustin.piqueres@gmail.com", external=True)
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
