import pathlib

import pytest
from jinja2 import Environment, FileSystemLoader

import build_library as bl


EXAMPLE_USER_DATA = {
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

def test_itemize():
    itemize1 = "- item1\n- item2\n"
    assert bl.itemize(["item1", "item2"]) == itemize1
    assert bl.itemize([""]) == ""
    assert bl.itemize([]) == ""
    assert bl.itemize(["hey"]) == "- hey\n"


def test_wrap_detailed():
    text = "<details><summary> Promoción: 2022 </summary><hr>this text</details>"
    assert text == bl.wrap_detailed(end_year="2022", text="this text")


def test_transform_strlist():
    assert ["link1", "link2"] == bl._transform_str_list("link1, link2")
    assert "" == bl._transform_str_list("")
    assert ["l1", "l2", "l3"] == bl._transform_str_list("l1,l2,,l3")
    assert "" == bl._transform_str_list(" ")


def test_itemize_field():
    tutors = bl.itemize_field(EXAMPLE_USER_DATA["tutors"])
    assert tutors == "- tutor1\n- tutor2\n"
    links = bl.itemize_field(EXAMPLE_USER_DATA["repository_links"])
    assert links == "- link1\n- link2\n"


def test_fill_student_entry():

    example = {
        "author": "author",
        "title": "title",
        "tutors": bl.itemize_field("tutor1, tutor2"),
        "abstract": "abstract",
        "fields": bl.itemize_field("field1, field2"),
        "memory_link": "memory",
        "repository_links": bl.itemize_field("link1, link2"),
        "email": "email",
        "gh_user": "gh_user",
    }
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template(bl.TEMPLATE_ENTRY)

    entry_content = template.render(**example)

    text = """# Autor

author

## Título

title

## Tutor/es

- tutor1
- tutor2


## Abstract

abstract

## Campos

- field1
- field2


## Memoria

memory

## Repositorio/s

- link1
- link2


## Contacto

- Correo: email
- [GitHub](https://github.com/gh_user)."""
    assert entry_content == text


def test_student_readme_name():
    assert "juan_malaga.md" == bl.student_readme_name("Juan Málaga")
    assert "numero_2-compuesto.md" == bl.student_readme_name("Número 2-compuesto")


def test_table_md():
    tabular_data = {"Alumno": ["1"], "Título": ["2"], "Enlace": ["3"]}
    table = bl.table_md(tabular_data)
    assert (
        table
        == "|   Alumno |   Título |   Enlace |\n|----------|----------|----------|\n|        1 |        2 |        3 |"
    )


def test_parse_md():
    pathfile = pathlib.Path.cwd() / "tests" / "sample_name.md"
    try:
        content = bl.parse_md(pathfile)
    except FileNotFoundError:
        print("Run this test from the root of the package: biblioteca-cidaen.")
        raise
    assert isinstance(content, dict)
    assert content["author"] == "Autor"
    assert content["title"] == "Tu Título"
    assert isinstance(content["link"], pathlib.Path)


def test_get_references():
    import tempfile

    with tempfile.TemporaryDirectory() as dirname:
        worksdir = pathlib.Path(dirname) / "trabajos"
        worksdir.mkdir()
        template = bl.get_template(bl.TEMPLATE_ENTRY)
        for p in (
            pathlib.Path("2022") / "name1.md",
            pathlib.Path("2022") / "name2.md",
            pathlib.Path("2024") / "name3.md",
        ):
            fp = worksdir / p
            if not fp.parent.exists():
                fp.parent.mkdir()
            bl.write_file(fp, template.render(**EXAMPLE_USER_DATA))
        print("contents: ", list(worksdir.glob("*/*.md")))
        refs = bl.get_references(str(worksdir / "*/*.md"))

    assert len(refs.keys()) == 2
    assert len(refs["2022"]) == 2
    assert len(refs["2024"]) == 1
    assert isinstance(refs["2022"][0], dict)


def test_md_links():
    assert bl._to_md_links("") == ""
    assert bl._to_md_links(" ") == ""
    assert bl._to_md_links("link1") == '- [repository_1](link1)\n'
    assert bl._to_md_links("link1, link2") == '- [repository_1](link1)\n- [repository_2](link2)\n'
    assert bl._to_md_links("link1", base_name="cosa") == '- [cosa_1](link1)\n'


def test_prepare_data():
    ready = bl.prepare_data(EXAMPLE_USER_DATA)
    assert len(ready) == 9
    assert ready["fields"] == '- field1\n- field2\n'
    assert ready["abstract"] == EXAMPLE_USER_DATA["abstract"]
    assert ready["repository_links"] == '- [repository_1](link1)\n- [repository_2](link2)\n'
