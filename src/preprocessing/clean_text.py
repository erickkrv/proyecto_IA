import re

def clean_text(texto):
    # pasar a minúsculas
    texto = texto.lower()

    # eliminar placeholders {{...}}
    texto = re.sub(r"\{\{.*?\}\}", "", texto)

    # eliminar caracteres especiales
    texto = re.sub(r"[^a-zA-Z\s]", "", texto)

    return texto