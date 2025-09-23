#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re, unicodedata, shutil

BASE = Path("apuntes")

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def slugify(s):
    s2 = strip_accents(s).lower()
    s2 = re.sub(r"[^a-z0-9]+", "-", s2).strip("-")
    return s2 or "curso"

def main():
    if not BASE.exists():
        print("No encuentro /apuntes"); return
    ren = 0
    for anio in sorted(BASE.glob("anio-*")):
        for sem in sorted(anio.glob("sem-*")):
            for curso_dir in list(sem.iterdir()):
                if not curso_dir.is_dir():
                    continue
                human = curso_dir.name
                slug = slugify(human)
                if human == slug:
                    # ya está en slug
                    # aseguremos que tenga title.txt con el nombre humano (por si no existe)
                    tt = curso_dir / "title.txt"
                    if not tt.exists():
                        tt.write_text(human, encoding="utf-8")
                    continue
                target = sem / slug
                target.mkdir(parents=True, exist_ok=True)
                # mover contenido
                for p in curso_dir.iterdir():
                    shutil.move(str(p), str(target / p.name))
                # guardar nombre bonito
                (target / "title.txt").write_text(human, encoding="utf-8")
                # borrar carpeta antigua (si queda vacía)
                try:
                    curso_dir.rmdir()
                except OSError:
                    pass
                print(f"✓ {human}  →  {target.name}")
                ren += 1
    print(f"\nListo. Carpetas renombradas: {ren}")

if __name__ == "__main__":
    main()
