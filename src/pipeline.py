from utils.load_data import cargar_dataset
from preprocessing.clean_text import clean_text
from preprocessing.tokenizer import tokenize
from model.vectorizer import build_vocab, text_to_bow
import json
import os

def preprocess_text(texto):
    texto = clean_text(texto)
    tokens = tokenize(texto)
    return tokens


def ejecutar_pipeline():
    print("Cargando dataset...")
    textos, categorias = cargar_dataset()

    print("Preprocesando textos...")
    textos_procesados = [preprocess_text(t) for t in textos]

    print("Construyendo vocabulario...")
    vocab = build_vocab(textos_procesados)

    print("Convirtiendo a vectores...")
    X = [text_to_bow(tokens, vocab) for tokens in textos_procesados]
    y = categorias

    # Guardar vocabulario
    os.makedirs("models", exist_ok=True)
    with open("models/vocab.json", "w") as f:
        json.dump(vocab, f)

    # Guardar dataset vectorizado
    os.makedirs("results", exist_ok=True)
    with open("results/dataset_vectorizado.json", "w") as f:
        json.dump({"X": X, "y": y}, f)

    print("PROCESO COMPLETADO")
    print("Total datos:", len(X))
    print("Tamaño vocabulario:", len(vocab))


if __name__ == "__main__":
    ejecutar_pipeline()