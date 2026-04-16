import sys
import os
import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Agregar src/ al path para poder importar los módulos del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "..", "src")
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")
sys.path.insert(0, SRC_DIR)

# Importar el pipeline de preprocesamiento 
from pipeline import preprocess_text

# Importar la función de vectorización 
from model.vectorizer import text_to_bow

# Importar el clasificador
from model.naive_bayes import NaiveBayesMultinomial


# --- Cargar vocabulario ---
# Este archivo fue generado por el pipeline de preprocesamiento
with open(os.path.join(MODELS_DIR, "vocab.json"), "r", encoding="utf-8") as f:
    vocab = json.load(f)

# --- Cargar modelo entrenado ---
modelo = NaiveBayesMultinomial()
modelo.load(os.path.join(MODELS_DIR, "naive_bayes_model.json"))


app = FastAPI()

# Archivos estáticos (CSS, JS)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)

# Templates Jinja2
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/predict")
async def predict(request: Request):
    try:
        data = await request.json()
        texto = data.get("texto", "").strip()

        if not texto:
            return JSONResponse(
                {"error": "El texto no puede estar vacío."},
                status_code=400,
            )

        # Paso 1: limpiar y tokenizar usando el pipeline existente
        tokens = preprocess_text(texto)

        # Paso 2: convertir los tokens a un vector Bag of Words
        vector = text_to_bow(tokens, vocab)

        # Paso 3: predecir la categoría con el modelo entrenado
        categoria = modelo.predict(vector)
        probabilidades = modelo.predict_proba(vector)

        return JSONResponse({"categoria": categoria, "probabilidades": probabilidades})

    except Exception as e:
        return JSONResponse(
            {"error": f"Ocurrió un error al procesar la solicitud: {str(e)}"},
            status_code=500,
        )
