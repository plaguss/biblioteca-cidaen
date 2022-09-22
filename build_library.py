"""Script para generar el README.md principal. """

import glob
import pathlib
from typing import *

from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode
from tabulate import tabulate

TEMPLATE_ENTRY = "entrada_alumno.md_t"
TEMPLATE_README = "README.md_t"


def itemize(elements: List[str]) -> str:
    """Transforms a list of str to an item list in markdown format."""
    items = ""
    if elements == [""] or elements == []:
        return ""
    for el in elements:
        items += f"- {el}\n"
    return items


def wrap_detailed(end_year: str = "", text: str = "") -> str:
    """Wraps text in html so the text appears clickable."""
    return (
        "<details>"
        f"<summary> Promoción: {end_year} </summary>"
        "<hr>"
        f"{text}"
        "</details>"
    )


def _transform_str_list(strlist: str) -> List[str]:
    """Transforms a str which represents a list, to a list of str."""
    if strlist == "":
        return strlist
    strlist = strlist.strip()
    return [s.strip() for s in strlist.split(",") if s != ""]


def itemize_field(strlist: str) -> str:
    """Generates a markdown item list from a list of comma separated string."""
    return itemize(_transform_str_list(strlist))


def student_readme_name(name: str) -> str:
    """Generates the filename for the student's readme. """
    name = name.strip()
    name = unidecode(name).lower()
    return f"{name.replace(' ', '_')}.md"


def link_md(name: str, path: str) -> str:
    """Creates a markdown link. """
    return f"[{name}]({path})"


def table_md(tabular_data: Dict[str, List[str]]) -> str:
    """Generates a table in markdown format to be inserted in a README.md. """
    return tabulate(tabular_data, headers="keys", tablefmt="github")


def parse_md(file: pathlib.Path) -> Dict[str, str]:
    """Reads a markdown file of a student and extracts the relevant info. """
    with open(file, "r") as f:
        return f.read()

# Para localizar las nuevas entradas
works = [pathlib.Path(p) for p in glob.glob("./trabajos/**/*.md", recursive=True)]
# print(f"Paths: {works}")
