import pytest
from jinja2 import Environment, FileSystemLoader

import build_library as bl


def test_itemize():
    itemize1 = "- item1\n- item2\n"
    assert bl.itemize(["item1", "item2"]) == itemize1
    assert bl.itemize([""]) == ""
    assert bl.itemize([]) == ""


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
        "tutors": "tutor1, tutor2",
        "abstract": "abstract",
        "fields": "field1, field2",
        "memory_link": "memory",
        "repository_links": "link1, link2",
        "email": "email",
        "gh_user": "gh_user",
    }
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template(bl.TEMPLATE_ENTRY)

    entry_content = template.render(**example)
    assert entry_content == 2


def test_student_readme_name():
    assert "juan_malaga.md" == bl.student_readme_name("Juan Málaga")
    assert "numero_2-compuesto.md" == bl.student_readme_name("Número 2-compuesto")
    