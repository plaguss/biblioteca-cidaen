"""Script para generar el README.md principal. """

import argparse
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
PROMPT_PREFIX = "> "

from rich.console import Console
from rich.style import Style

console = Console()

style = Style(color="#70c4fd", bold=True)


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
        f"\n\n{text}\n\n"
        "</details>\n\n"
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


#regex_author = re.compile(r"# Autor(.*?)## Título", re.UNICODE)
#regex_title = re.compile(r"## Título(.*?)## Tutor/es", re.UNICODE)
regex_author = re.compile(r"# Autor(.*?)## Title", re.UNICODE)
regex_title = re.compile(r"## Title(.*?)## Tutor/es", re.UNICODE)


def parse_md(file: pathlib.Path) -> Dict[str, Union[str, pathlib.Path]]:
    """Reads a markdown file of a student and extracts the relevant info.
    {"author": "autor", "title": "title", "link": "path"}
    """
    with open(file, "r") as f:
        content = f.read()

    content_ = content.replace("\n", "")  # Remove \n prior to regex search
    content_ = content_.replace("## Título", "## Title")  # Check for windows GitHub actions runner

    author = re.search(regex_author, content_).group(1)
    title = re.search(regex_title, content_).group(1)

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
        name = pathlib.Path(d).name
        # field = f"[{base_name + '_' + str(i + 1)}]({d})"
        field = f"[{name}]({d})"
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
    data["memory_link"] = _to_md_links(data["memory_link"])
    data["repository_links"] = _to_md_links(data["repository_links"])
    return data


def generate_entry(
    data: Dict[str, str], dest_dir: pathlib.Path = ROOT_DIR / "trabajos/2022"
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
    if not dest_dir.is_dir():
        dest_dir.mkdir()
    write_file(str(filename), template.render(**data))
    console.print()
    console.print(f"Tu entrada se ha generado en: {str(filename)}. \n")


def get_parser() -> argparse.ArgumentParser:
    """Generates the CLI for of the program."""
    description = (
        "\n"
        "Crea tu propia entrada.\n"
        "\n"
        "Ejecuta este programa y rellena los distintas preguntas\n"
        "para compartir tu trabajo de final de máster con el resto\n"
        "de tus compañeros de CIDaEN :)\n"
    )
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS]", description=description
    )
    parser.add_argument(
        "-l",
        "--library",
        action="store_true",
        dest="library",
        default=False,
        help=(
            "Ejecuta con esta opción para regenerar el README principal, "
            "no lanza el cuestionario. Por defecto False"
        ),
    )
    return parser


# Validator functions
def nonempty(x: str) -> str:
    if not x:
        raise ValueError("Por favor introduce algún campo.")
    return x


def allow_empty(x: str) -> str:
    return x


def do_prompt(
    text: str, default: str = "", validator: Callable[[str], Any] = allow_empty
) -> Union[str, bool]:
    """Loop of input values to be given by the user."""
    while True:
        prompt = PROMPT_PREFIX + text + ": "

        # x = term_input(prompt).strip()
        x = console.input(f"[bold #70c4fd]{prompt}").strip()

        if default and not x:
            x = default
        try:
            x = validator(x)
        except ValueError as err:
            print("* " + str(err))
            continue

        break

    return x


def questionnaire() -> Dict[str, str]:
    """Asks the user for the info to be added.

    The current info includes:
    * autor (author)
    * año de promoción (year)
    * título (title)
    * tutores (tutors)
    * campos (fields)
    * memoria (memory_link)
    * repositorio (repository_links)
    * email (email)
    * usuario_github (gh_user)
    """
    # TODO: PRETTIFY WITH rich
    console.print("Bienvenido al registro de TFMs de CIDaEN.", style=style)
    console.print()
    console.print("Por favor, responde a las siguientes preguntas ", style=style)
    console.print("para incluir información de tu trabajo.", style=style)
    console.print()
    console.print("Si un campo no quieres informarlo, pulsa Enter", style=style)
    console.print("y se asumirá el valor por defecto (aparecerá vacío).", style=style)
    console.rule()

    questions = {}
    # Añadir validadores para los distintos campos
    console.print()
    questions["author"] = do_prompt("Introduce tu nombre")
    console.print()
    questions["year"] = do_prompt(
        "¿Cuál es el año de tu promoción? \n"
        "Si cursaste la promoción 2021-2022, \n"
        "introduce 2022"
    )
    console.print()
    questions["title"] = do_prompt("Título del trabajo")
    console.print()
    questions["tutors"] = do_prompt(
        "Tutor/es. Si has tenido más de uno, \n"
        "introdúcelos separados por coma, como\n"
        "se muestra a continuación [tutor1, tutor2]"
    )
    console.print()
    questions["abstract"] = do_prompt(
        "Abstract. Puedes directamente copiar y, \n" "pegar el resumen de tu trabajo."
    )
    console.print()
    questions["fields"] = do_prompt(
        "Campo/s con los que se relaciona tu trabajo. \n"
        "Si has tenido más de uno, introdúcelos \n"
        "separados por coma: [deep_learning, cloud_computing]"
    )
    console.print()
    questions["memory_link"] = do_prompt(
        "Si tu trabajo lo tienes expuesto \n"
        "de forma pública (por ejemplo, un .pdf \n"
        "en un repositorio tuyo público), y quieres \n"
        "dar acceso para que otros lo lean, escribe \n"
        "el enlace aquí"
    )
    console.print()
    questions["repository_links"] = do_prompt(
        "¿Tienes el código compartido de forma \n"
        "pública en un repositorio de GitHub \n"
        ", y quieres dar acceso para que otros lo puedan \n"
        "leer? Introduce el enlace aquí. Si tienes más de \n"
        "un repositorio, introdúcelos como una lista \n"
        "separada por comas [repo1, repo2]"
    )
    console.print()
    questions["email"] = do_prompt(
        "¿Quieres facilitar tu correo por posibles \n" "consultas?"
    )
    console.print()
    questions["gh_user"] = do_prompt(
        "¿Quieres compartir tu repositorio de GitHub? \n" "Introduce tu usuario"
    )
    console.print()
    console.print("Gracias!", style=style)

    console.rule()

    return questions


def generate_readme():
    """Creates the README file in the root of the project."""
    refs = get_references("./trabajos/**/*.md")
    years = sorted(refs.keys())
    tfms = ""
    content = ""
    registers = col.defaultdict(list)
    for year in years:
        for register in refs[year]:
            registers["author"].append(register["author"])
            registers["title"].append(register["title"])
            registers["link"].append(link_md("enlace", "./" + str(register["link"])))

        content = table_md(registers)
        tfms += wrap_detailed(year, content)
        registers = col.defaultdict(list)  # Restart the content to avoid reprinting it

    readme_template = get_template(TEMPLATE_README)

    write_file(str(ROOT_DIR / "README.md"), readme_template.render({"tfms": tfms}))

    console.print("README actualizado!")


def main(argv: Optional[List[str]]) -> int:
    # Function adapted from: https://github.com/sphinx-doc/sphinx/blob/5.x/sphinx/cmd/quickstart.py#L589
    parser = get_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as err:
        return err.code

    args = vars(args)

    if args["library"]:
        try:
            generate_readme()  # Write the markdown and exit.
            return 0
        except Exception as exc:
            print("Error inesperado: ")
            raise exc
            # return 1

    try:
        info = questionnaire()
        generate_entry(info, dest_dir=ROOT_DIR / "trabajos" / info["year"])
        return 0
    except KeyboardInterrupt:
        print()
        print("Se interrumpió.")
        return 130  # 128 + SIGINT


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv[1:]))
