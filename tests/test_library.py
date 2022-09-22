import pathlib
import pytest
from jinja2 import Environment, FileSystemLoader

import build_library as bl


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


def test_itemize_field():
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
    tutors = bl.itemize_field(example["tutors"])
    assert tutors == "- tutor1\n- tutor2\n"
    links = bl.itemize_field(example["repository_links"])
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
    print(str(entry_content))
    text = ("""# Autor

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
- [GitHub](https://github.com/gh_user).""")
    assert entry_content == text


def test_student_readme_name():
    assert "juan_malaga.md" == bl.student_readme_name("Juan Málaga")
    assert "numero_2-compuesto.md" == bl.student_readme_name("Número 2-compuesto")
    

def test_table_md():
    tabular_data = {"Alumno": ["1"], "Título": ["2"], "Enlace": ["3"]}
    table = bl.table_md(tabular_data)
    assert table == '|   Alumno |   Título |   Enlace |\n|----------|----------|----------|\n|        1 |        2 |        3 |'


def test_parse_md():
    try:
        content = bl.parse_md(pathlib.Path.cwd() / "tests" / "sample_name.md")
    except FileNotFoundError:
        print("Run this test from the root of the package: biblioteca-cidaen.")
        raise
    assert content == 1
