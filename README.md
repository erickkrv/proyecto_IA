# Clasificación de Texto con Naïve Bayes Multinomial

**Proyecto 1 — Inteligencia Artificial | Primer Semestre 2026**

**Autores:** Christopher Yuman · Susana García · Erick Rivas

---

## Descripción general

Este proyecto implementa un sistema de clasificación automática de solicitudes de soporte al cliente utilizando el algoritmo **Naïve Bayes Multinomial**, construido completamente desde cero en Python, sin el uso de librerías de machine learning (scikit-learn, PyTorch, etc.).

El sistema recibe como entrada el texto libre de una solicitud de cliente y predice a cuál de las 11 categorías de soporte pertenece. Incluye un pipeline completo de procesamiento de lenguaje natural (NLP), un clasificador probabilístico con suavizado de Laplace, validación cruzada con K-Folds y una interfaz web funcional para realizar predicciones en tiempo real.

---

## Dataset

**Fuente:** [Bitext Customer Support Dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) — Hugging Face

| Campo | Descripción |
|---|---|
| `instruction` | Texto de entrada (solicitud del cliente) |
| `category` | Etiqueta de clase objetivo |

- **Total de instancias:** 26,872
- **Número de categorías:** 11

### Categorías

`ACCOUNT` · `CANCEL` · `CONTACT` · `DELIVERY` · `FEEDBACK` · `INVOICE` · `ORDER` · `PAYMENT` · `REFUND` · `SHIPPING` · `SUBSCRIPTION`

---

## Arquitectura del sistema

El proyecto está organizado en tres componentes principales, cada uno desarrollado de forma independiente e integrado al final:

### 1. Pipeline de preprocesamiento (`src/`)

Transforma el texto crudo en vectores numéricos mediante las siguientes etapas:

1. **Limpieza** — conversión a minúsculas, eliminación de placeholders `{{...}}` y caracteres no alfabéticos
2. **Tokenización** — división del texto en tokens individuales
3. **Eliminación de stopwords** — remoción de palabras sin carga semántica (*the, is, about...*)
4. **Stemming** — reducción de cada palabra a su raíz morfológica (*cancelling → cancel*)
5. **Construcción de vocabulario** — diccionario `{palabra: índice}` de 2,506 términos únicos
6. **Vectorización Bag of Words** — representación de cada documento como vector de frecuencias

### 2. Clasificador Naïve Bayes (`src/model/`)

Implementación del clasificador multinomial con las siguientes características:

- **Probabilidad a priori:** `log P(clase)` estimada a partir de la distribución de clases en el conjunto de entrenamiento
- **Probabilidad condicional:** `log P(palabra | clase)` con **suavizado de Laplace** (`α = 1.0`) para evitar probabilidades cero
- **Predicción:** regla de decisión mediante suma de logaritmos, evitando underflow numérico
- **Persistencia:** el modelo se serializa y carga en formato JSON

La evaluación se realiza mediante **5-Fold Cross Validation** sobre el conjunto completo de datos, reportando Accuracy, Precision, Recall y F1-Score por categoría.

### 3. Interfaz web (`web/`)

Aplicación web construida con **FastAPI** que expone un endpoint `POST /predict`. El frontend en HTML/CSS/JS permite al usuario ingresar texto y visualizar la categoría predicha en tiempo real, sin reentrenar ni modificar el modelo.

**Flujo de una predicción:**

```
Usuario → POST /predict → preprocess_text() → text_to_bow() → NaiveBayes.predict() → JSON
```

---

## Estructura del repositorio

```
proyecto_IA/
├── docs/
│   └── documentacion_IA.pdf        # Documentación del proyecto
├── models/
│   ├── vocab.json                  # Vocabulario generado por el pipeline
│   └── naive_bayes_model.json      # Pesos del modelo entrenado
├── results/
│   └── dataset_vectorizado.json    # Vectores X y etiquetas y
├── src/
│   ├── pipeline.py                 # Script principal de preprocesamiento
│   ├── train.py                    # Script de entrenamiento y evaluación
│   ├── preprocessing/
│   │   ├── clean_text.py           # Limpieza de texto
│   │   └── tokenizer.py            # Tokenización, stopwords y stemming
│   ├── model/
│   │   ├── naive_bayes.py          # Clasificador Naïve Bayes Multinomial
│   │   └── vectorizer.py           # Construcción de vocabulario y BoW
│   ├── evaluation/
│   │   ├── k_folds.py              # Validación cruzada K-Folds
│   │   └── metrics.py              # Accuracy, Precision, Recall, F1, matriz de confusión
│   └── utils/
│       └── load_data.py            # Carga del dataset desde Hugging Face
├── web/
│   ├── app.py                      # Servidor FastAPI
│   ├── templates/
│   │   └── index.html              # Interfaz web
│   └── static/
│       ├── css/styles.css
│       └── js/app.js
├── requirements.txt
└── README.md
```

---

## Instalación y ejecución

### Requisitos previos

- Python 3.9 o superior
- pip

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd proyecto_IA
```

### 2. Crear y activar un entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias del proyecto son:

| Paquete | Uso |
|---|---|
| `datasets` | Descarga del dataset desde Hugging Face |
| `nltk` | Stopwords y stemming |
| `fastapi` | Servidor web del backend |
| `uvicorn` | Servidor ASGI para FastAPI |
| `jinja2` | Motor de plantillas HTML |
| `python-multipart` | Soporte para formularios en FastAPI |

### 4. Ejecutar el pipeline de preprocesamiento

> **Nota:** Este paso solo es necesario si los archivos `models/vocab.json` y `results/dataset_vectorizado.json` no están presentes en el repositorio.

```bash
python src/pipeline.py
```

Genera: `models/vocab.json` y `results/dataset_vectorizado.json`.

### 5. Entrenar el modelo

> **Nota:** Este paso solo es necesario si `models/naive_bayes_model.json` no está presente en el repositorio.

```bash
python src/train.py
```

Genera: `models/naive_bayes_model.json`. Imprime las métricas de evaluación por fold y por categoría.

### 6. Iniciar la aplicación web

```bash
uvicorn web.app:app --reload
```

Abrir en el navegador: **`http://localhost:8000`**

---

## Resultados

### Validación cruzada (5-Fold)

| Fold | Accuracy |
|---|---|
| Fold 1 | 0.9913 |
| Fold 2 | 0.9922 |
| Fold 3 | 0.9920 |
| Fold 4 | 0.9911 |
| Fold 5 | 0.9894 |
| **Promedio** | **0.9912** |
| Varianza | 0.000001 |
| Diferencia máx–mín | 0.0028 |

La baja varianza entre folds indica que el modelo generaliza de forma estable y no presenta sobreajuste significativo.

### Métricas por categoría

| Categoría | Precision | Recall | F1-Score |
|---|---|---|---|
| ACCOUNT | 0.9978 | 0.9982 | 0.9980 |
| CANCEL | 1.0000 | 0.9958 | 0.9979 |
| CONTACT | 0.9995 | 0.9980 | 0.9987 |
| DELIVERY | 0.9799 | 0.9283 | 0.9534 |
| FEEDBACK | 0.9960 | 0.9990 | 0.9975 |
| INVOICE | 0.9990 | 0.9910 | 0.9950 |
| ORDER | 0.9766 | 0.9925 | 0.9845 |
| PAYMENT | 0.9955 | 0.9975 | 0.9965 |
| REFUND | 0.9987 | 0.9957 | 0.9972 |
| SHIPPING | 0.9680 | 0.9970 | 0.9822 |
| SUBSCRIPTION | 0.9980 | 0.9990 | 0.9985 |
| **Macro F1** | | | **0.9909** |

Las categorías con menor desempeño (DELIVERY, SHIPPING, ORDER) presentan mayor ambigüedad semántica entre sí, lo cual es esperable en un clasificador basado en frecuencia de términos.

---

## Restricciones del proyecto

- No se utilizan librerías de machine learning (scikit-learn, PyTorch, TensorFlow, etc.)
- No se utilizan APIs externas de procesamiento de lenguaje
- El clasificador está implementado completamente en Python estándar
- La persistencia del modelo se realiza en JSON plano, sin pickle ni formatos binarios
