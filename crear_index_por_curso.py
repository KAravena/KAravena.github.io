#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crea un index.qmd en cada carpeta de curso: /apuntes/anio-*/sem-*/<curso>/index.qmd
- No sobreescribe si ya existe.
- Toma el título humano desde title.txt (si existe); si no, usa el nombre de carpeta.
- Pone banner con ruta a /resources/imagenes/cursos/<slug>.jpg (puedes reemplazar luego).
- Activa un listing de los .qmd del curso (excluye index.qmd).
"""

from pathlib import Path
import re
import unicodedata

ROOT = Path(".")
BASE = ROOT / "apuntes"

def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )

def slugify(texto: str) -> str:
    t = strip_accents(texto).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "curso"

def course_title(course_dir: Path) -> str:
    tfile = course_dir / "title.txt"
    if tfile.exists():
        return tfile.read_text(encoding="utf-8").strip() or course_dir.name
    return course_dir.name

def detect_codes(course_dir: Path):
    """
    Devuelve (anio_code, sem_code) tomados del path: .../apuntes/anio-*/sem-*/<curso>
    """
    try:
        sem_code = course_dir.parent.name          # sem-XX
        anio_code = course_dir.parent.parent.name  # anio-X
        return anio_code, sem_code
    except Exception:
        return "anio-?", "sem-??"

TEMPLATE = """---
title: "{TITLE}"
description: "Síntesis, conceptos clave y bibliografía."
categories: [{ANIO}, {SEM}]
image: /resources/imagenes/cursos/{BANNER}
title-block-banner: true
page-layout: full

listing:
  - id: apuntes-curso
    contents:
      - "*.qmd"
      - "!index.qmd"
    type: table
    sort: "date desc"
    fields: [title, author, date, description]
    filter-ui: true
    sort-ui: true
---

## Sobre este curso
Breve descripción del curso o indicaciones para aportar (formato, citas, etc.).

### Apuntes del curso
::: {{#apuntes-curso}}
:::
"""

def main():
    if not BASE.exists():
        print("No encuentro la carpeta 'apuntes/'. ¿Estás en la raíz del repo?")
        return

    creados = 0
    for anio_dir in BASE.glob("anio-*"):
        for sem_dir in anio_dir.glob("sem-*"):
            for course_dir in sem_dir.iterdir():
                if not course_dir.is_dir():
                    continue
                index_qmd = course_dir / "index.qmd"
                if index_qmd.exists():
                    continue  # no pisar

                titulo = course_title(course_dir)
                anio_code, sem_code = detect_codes(course_dir)
                banner_slug = slugify(titulo) + ".jpg"  # cambia a .png si prefieres

                content = TEMPLATE.format(
                    TITLE=titulo.replace('"', '\\"'),
                    ANIO=anio_code,
                    SEM=sem_code,
                    BANNER=banner_slug
                )
                index_qmd.write_text(content, encoding="utf-8")
                creados += 1
                print(f"✔ Creado: {index_qmd}")

    print(f"\nListo ✅  Se crearon {creados} index.qmd")

if __name__ == "__main__":
    main()
