# md.py



```python
import os

carpeta_origen = "."
carpeta_destino = "Archivos en Markdown"

os.makedirs(carpeta_destino, exist_ok=True)

for archivo in os.listdir(carpeta_origen):
    if archivo.endswith(".py"):
        ruta_py = os.path.join(carpeta_origen, archivo)
        nombre_sin_extension = os.path.splitext(archivo)[0]
        ruta_md = os.path.join(carpeta_destino, f"{nombre_sin_extension}.md")

        with open(ruta_py, "r", encoding="utf-8") as f_py:
            lineas = f_py.readlines()

        intro = []
        codigo = []
        leyendo_intro = True

        for linea in lineas:
            if leyendo_intro and (linea.strip().startswith("#") or linea.strip() == ""):
                intro.append(linea.strip("#").strip())  # Quita el símbolo de comentario
            else:
                leyendo_intro = False
                codigo.append(linea)

        texto_intro = "\n".join(intro).strip()
        bloque_codigo = "".join(codigo)

        contenido_md = f"# {archivo}\n\n{texto_intro}\n\n```python\n{bloque_codigo}\n```"

        with open(ruta_md, "w", encoding="utf-8") as f_md:
            f_md.write(contenido_md)

print("✅ Archivos .py convertidos a .md con introducción comentada.")

```