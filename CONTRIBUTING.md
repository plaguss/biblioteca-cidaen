# Guía para compartir tu trabajo

## 1. Crea un fork de este proyecto

En esta [guía de GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) puedes ver como es el proceso en caso de que no lo conozcas.

- *¿Que es un [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks)?*

## 2. Prepara el proyecto

Crea un entorno virtual:

```bash
$ python -m venv venv
```

Instala las dependencias para poder ejecutar el programa:

```bash
$ pip install -r requirements/requirements.txt
```

## 3. Ejecuta el programa

Solo necesitas ejecutar un script en tu consola:

```bash
$ python build_library.py
```

Este te hará una serie de preguntas que puedes ir rellenando. Solo tienes que rellenar y pulsar `Enter` a cada pregunta. Si alguna de ella no quieres rellenarla, simplemente pulsa `Enter` y quedará vacía.

A continuación puedes ver video del funcionamiento:

[![asciicast](https://asciinema.org/a/gahwh0wpNmdPKDOIrkRqzkRfv.svg)](https://asciinema.org/a/gahwh0wpNmdPKDOIrkRqzkRfv)


## 4. Crea un Pull Request al repositorio

Haz un pull request (PR) a la rama `main` del repositorio. Una vez se haga el merge, tu nueva entrada aparecerá en el [README.md](README.md) principal, en el desplegable del año de tu promoción :smile:.

- *¿Que és un [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request#changing-the-branch-range-and-destination-repository)?*
