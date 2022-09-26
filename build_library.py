"""Script para generar el README.md principal. """

import collections as col
import glob
import os
import pathlib
import re
from typing import *

from jinja2 import Environment, FileSystemLoader, Template
from tabulate import tabulate
from unidecode import unidecode

TEMPLATE_ENTRY = "entrada_alumno.md_t"
TEMPLATE_README = "README.md_t"
ROOT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
NOT_INFORMED_FIELD = "Not informed"


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
    strlist = strlist.strip()
    if strlist == "":
        return strlist
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


def _to_md_links(content: str, base_name: str = "repository") -> str:
    """Transforms the content of a str input to be in the form of a
    markdown link.
    It's used to prepare the repository links from the user, but may
    be useful for other cases.
    """
    data = _transform_str_list(content)
    if len(data) == 0:
        return ""  # NOT_INFORMED_FIELD

    items = len(data)
    transformed = ""
    for i, d in enumerate(data):
        field = f"[{base_name + '_' + str(i + 1)}]({d})"
        # Adds a comma only if there are more than one element and
        # all but the last item.
        if i >= 0 or i < items - 1:
            field += ", "
        transformed += field

    return itemize_field(transformed)


def prepare_data(data: Dict[str, str]) -> Dict[str, str]:
    """Updates the user info to be directly markdown ready."""
    # TODO: Validate the entries for the case of no content
    data["tutors"] = itemize_field(data["tutors"])
    data["fields"] = itemize_field(data["fields"])
    data["repository_links"] = _to_md_links(data["repository_links"])
    return data


def generate_entry(
    data: Dict[str, str], dest_dir: pathlib.Path = ROOT_DIR / "templates/2022"
):
    """Creates a markdown file with the info of a student obtained
    from the console.
    Needs the info as a dict to be parsed to markdown strings, and the destination
    directory.
    By default will write to templates and the promotion of 2022,
    the year may be obtained from get_references function.
    """
    data = prepare_data(data)
    template = get_template(TEMPLATE_ENTRY)
    author_renamed = student_readme_name(data["author"])
    filename = dest_dir / author_renamed
    write_file(str(filename), template.render(**data))
