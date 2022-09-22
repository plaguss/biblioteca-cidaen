import pytest

import build_library as bl


def test_itemize():
    itemize1 = "- item1\n- item2\n"
    assert bl.itemize(["item1", "item2"]) == itemize1
    assert bl.itemize([""]) == ""
    assert bl.itemize([]) == ""


def test_wrap_detailed():
    text = '<details><summary> Promoción: 2022 </summary><hr>this text</details>'
    assert text == bl.wrap_detailed(end_year="2022", text="this text")
