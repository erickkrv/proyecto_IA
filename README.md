# Proyecto 1 — Clasificación de Texto con Naïve Bayes

Clasificador automático de solicitudes de soporte al cliente implementado desde cero, sin uso de librerías de machine learning. El sistema aplica un pipeline completo de NLP para transformar texto crudo en predicciones de categoría.

---

## Dataset

**Bitext Customer Support Dataset** — Hugging Face

| Campo | Uso |
|---|---|
| `instruction` | Texto de entrada (solicitud del cliente) |
| `category` | Etiqueta de clase (categoría) |

- Total de instancias: **26,872**
- Número de categorías: **11**

### Categorías del modelo

`ACCOUNT` · `CANCEL` · `CONTACT` · `DELIVERY` · `FEEDBACK` · `INVOICE` · `ORDER` · `PAYMENT` · `REFUND` · `SHIPPING` · `SUBSCRIPTION`

---

## Estructura del proyecto

```
proyecto_IA/
├── data/
│   ├── raw/                  # Datos originales (sin procesar)
│   └── processed/            # Datos procesados
├── models/
│   ├── vocab.json            # Vocabulario global generado por Persona 1
│   └── naive_bayes_model.json  # Modelo entrenado por Persona 2
├── results/
│   └── dataset_vectorizado.json  # Vectores X e etiquetas y
├── src/
│   ├── pipeline.py           # Pipeline de preprocesamiento (Persona 1)
│   ├── train.py              # Script de entrenamiento (Persona 2)
│   ├── preprocessing/
│   │   ├── clean_text.py     # Limpieza de texto
│   │   └── tokenizer.py      # Tokenización, stopwords y stemming
│   ├── model/
│   │   ├── naive_bayes.py    # Clasificador Naïve Bayes Multinomial
│   │   └── vectorizer.py     # Construcción de vocabulario y Bag of Words
│   ├── evaluation/
│   │   ├── k_folds.py        # Validación cruzada K-Folds
│   │   └── metrics.py        # Accuracy, Precision, Recall, F1, Matriz de confusión
│   └── utils/
│       └── load_data.py      # Carga del dataset desde Hugging Face
├── web/
│   ├── app.py                # Servidor FastAPI (Persona 3)
│   ├── templates/
│   │   └── index.html        # Interfaz web
│   └── static/
│       ├── css/styles.css
│       └── js/app.js
├── requirements.txt
└── README.md
```

---

## Personas y responsabilidades

### Persona 1 — Preprocesamiento de datos

Transforma el texto crudo del dataset en vectores numéricos listos para el entrenamiento.

**Pipeline (`src/pipeline.py`):**

1. **Limpieza** — minúsculas, eliminación de placeholders `{{...}}` y caracteres especiales
2. **Tokenización** — división en palabras
3. **Eliminación de stopwords** — palabras sin valor semántico (*the, is, about...*)
4. **Stemming** — reducción a raíz (*cancelling → cancel*)
5. **Vocabulario** — diccionario `{palabra: índice}` con 2,506 palabras
6. **Bag of Words** — vector de frecuencias por documento

**Archivos generados:**
- `models/vocab.json`
- `results/dataset_vectorizado.json`

**Ejecución:**
```bash
python src/pipeline.py
```

---

### Persona 2 — Modelo Naïve Bayes

Implementa y entrena el clasificador multinomial desde cero, sin librerías de ML.

**Implementación (`src/model/naive_bayes.py`):**

- Probabilidad a priori: `log P(clase)`
- Probabilidad condicional: `log P(palabra | clase)` con suavizado de Laplace (`alpha=1.0`)
- Predicción: suma de logaritmos para evitar underflow numérico
- Persistencia: guardado y carga del modelo en formato JSON

**Validación (`src/evaluation/`):**

- 5-Fold Cross Validation sobre los 26,872 documentos
- Métricas por clase: Precision, Recall, F1-Score
- Matriz de confusión

**Ejecución:**
```bash
python src/train.py
```

---

### Persona 3 — Web e Integración

Construye la interfaz web que conecta el frontend con el pipeline de preprocesamiento y el modelo entrenado, sin reentrenar ni modificar las etapas anteriores.

**Flujo de una predicción:**

1. El usuario ingresa una solicitud en el formulario web
2. El frontend envía el texto al backend via `POST /predict`
3. El backend aplica `preprocess_text()` (Persona 1)
4. Convierte los tokens a vector con `text_to_bow()` y el vocabulario cargado
5. El modelo predice la categoría con `NaiveBayesMultinomial.predict()`
6. El resultado se devuelve como JSON y se muestra en pantalla

**Ejecución:**
```bash
uvicorn web.app:app --reload
```

Abrir en el navegador: `http://localhost:8000`

---

## Resultados del modelo

### 5-Fold Cross Validation

| Fold | Accuracy |
|---|---|
| Fold 1 | 0.9913 |
| Fold 2 | 0.9922 |
| Fold 3 | 0.9920 |
| Fold 4 | 0.9911 |
| Fold 5 | 0.9894 |
| **Promedio** | **0.9912** |
| Varianza | 0.000001 |
| Diferencia (Max-Min) | 0.0028 |

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

---

## Instalación y ejecución completa

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el pipeline de preprocesamiento (Persona 1)

```bash
python src/pipeline.py
```

Genera `models/vocab.json` y `results/dataset_vectorizado.json`.

### 3. Entrenar el modelo (Persona 2)

```bash
python src/train.py
```

Genera `models/naive_bayes_model.json`.

### 4. Iniciar la aplicación web (Persona 3)

```bash
uvicorn web.app:app --reload
```

Abrir `http://localhost:8000` en el navegador.

> Los pasos 1 y 2 solo se deben ejecutar una vez. Los archivos generados ya están incluidos en el repositorio.

---

## Restricciones del proyecto

- No se utilizan librerías de machine learning (scikit-learn, PyTorch, etc.)
- No se utilizan APIs externas
- El clasificador está implementado completamente desde cero en Python puro
- La persistencia del modelo se realiza en JSON plano (sin pickle)
