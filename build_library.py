"""Script para generar el README.md principal. """

import glob
import pathlib
from typing import *

from jinja2 import Environment, FileSystemLoader

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
    """Wraps text in html so the text appears clickable. """
    return (
        "<details>"
        f"<summary> Promoción: {end_year} </summary>"
        "<hr>"

        f"{text}"

        "</details>"
    )


environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template(TEMPLATE_ENTRY)

example = {
    "author": "author",
    "title": "title",
    "tutors": "tutor1, tutor2",
    "abstract": "abstract",
    "fields": "field1, field2",
    "memory_link": "memory",
    "repository_links": "link1, link2",
    "email": "email",
    "gh_user": "gh_user",
}

entry_content = template.render(**example)
print(entry_content)
# Para localizar las nuevas entradas
works = [pathlib.Path(p) for p in glob.glob("./trabajos/**/*.md", recursive=True)]
# print(f"Paths: {works}")
