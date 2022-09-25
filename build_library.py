"""Script para generar el README.md principal. """

import glob
import os
import pathlib
import re
import collections as col
from typing import *

from jinja2 import Environment, FileSystemLoader, Template
from tabulate import tabulate
from unidecode import unidecode

TEMPLATE_ENTRY = "entrada_alumno.md_t"
TEMPLATE_README = "README.md_t"
ROOT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))


def get_template(name: str = TEMPLATE_ENTRY) -> Template:
    environment = Environment(loader=FileSystemLoader(str(ROOT_DIR / "templates/")))
    return environment.get_template(name)


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
    """Generates the filename for the student's readme."""
    name = name.strip()
    name = unidecode(name).lower()
    return f"{name.replace(' ', '_')}.md"


def link_md(name: str, path: str) -> str:
    """Creates a markdown link."""
    return f"[{name}]({path})"


def table_md(tabular_data: Dict[str, List[str]]) -> str:
    """Generates a table in markdown format to be inserted in a README.md."""
    return tabulate(tabular_data, headers="keys", tablefmt="github")


def parse_md(file: pathlib.Path) -> Dict[str, Union[str, pathlib.Path]]:
    """Reads a markdown file of a student and extracts the relevant info.
    {"author": "autor", "title": "title", "link": "path"}
    """
    with open(file, "r") as f:
        content = f.read()

    regex_author = re.compile(r"# Autor(.*?)## Título")
    regex_title = re.compile(r"## Título(.*?)## Tutor/es")
    content = content.replace("\n", "")  # Remove \n prior to regex search

    author = re.search(regex_author, content).group(1)
    title = re.search(regex_title, content).group(1)

    return {"author": author, "title": title, "link": file}


def get_works(glob_path: str = "./trabajos/**/*.md") -> List[pathlib.Path]:
    """Retrieves the individual entries."""
    return [pathlib.Path(p) for p in glob.glob(glob_path, recursive=True)]


def write_file(fpath: str, content: str, newline: Optional[str] = None) -> None:
    """Writes a file named fpath with content."""
    with open(fpath, "w", encoding="utf-8", newline=newline) as f:
        f.write(content)


def get_references(
    glob_path: str = "./trabajos/**/*.md",
) -> DefaultDict[str, List[Dict[str, Union[str, pathlib.Path]]]]:
    """Gets the references to the individual files, the info to be
    used in the main readme file.
    """
    # TODO: Create an alias for the return type
    works = get_works(glob_path=glob_path)
    print("works: ", works)
    # Dict of List, with keys the years from the folders.
    d = col.defaultdict(list)
    for w in works:
        d[w.parent.name].append(parse_md(w))
    return d


def prepare_data(data: Dict[str, str]) -> Dict:
    pass


def generate_entry(data: Dict):
    """Creates a markdown file with the info of a student obtained
    from the console. """
    d = data
    template = get_template(TEMPLATE_ENTRY)
    filename = 1  # The name of the file comes from the data
    write_file(filename, template.render(**data))
