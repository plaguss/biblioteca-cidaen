"""Script para generar el README.md principal. """

import glob
import pathlib

from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("template_entrada.md")
print(template)

ejemplo = {
    "autor": "hey",
    "tutor": "",
    "resumen": 1,
    "memoria": 1,
    "autor": 1,
    "autor": 1,
}

content = template.render(
    student,
    max_score=max_score,
    test_name=test_name
)

# Para localizar las nuevas entradas
works = [pathlib.Path(p) for p in glob.glob("./trabajos/**/*.md", recursive=True)]
#print(f"Paths: {works}")
