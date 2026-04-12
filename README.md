# proyecto_IA
proyecto iA

---

# Preprocesamiento de Datos — Clasificación de Texto (Naïve Bayes)

## Rol: Persona 1 — Data & Preprocesamiento

Este módulo se encarga de transformar el texto crudo del dataset en datos estructurados y numéricos listos para el entrenamiento del modelo de clasificación.

---

## Objetivo

Convertir solicitudes de texto del dataset Bitext en vectores numéricos mediante técnicas de procesamiento de lenguaje natural (NLP), permitiendo que el modelo Naïve Bayes pueda procesarlos correctamente.

---

## Dataset utilizado

* **Nombre:** Bitext Customer Support Dataset
* **Fuente:** Hugging Face
* **Campos utilizados:**

  * `instruction` → texto de entrada
  * `category` → etiqueta (clase)

---

## Proceso de Preprocesamiento

### 1. Limpieza de texto

* Conversión a minúsculas
* Eliminación de placeholders (`{{...}}`)
* Eliminación de caracteres especiales

### 2. Tokenización

* División del texto en palabras (tokens)

### 3. Eliminación de stopwords

* Eliminación de palabras comunes sin valor semántico (ej: *the, is, about*)

### 4. Stemming

* Reducción de palabras a su raíz
* Ejemplo:

  * *cancelling → cancel*

### 5. Construcción de vocabulario

* Creación de un diccionario global:

  * palabra → índice

### 6. Representación Bag of Words

* Conversión de cada texto en un vector numérico
* Cada posición representa la frecuencia de una palabra

---

## Resultados

* Total de datos procesados: 26,872
* Tamaño del vocabulario: 2,506 palabras

---

## Archivos generados

* `models/vocab.json` → vocabulario global
* `results/dataset_vectorizado.json` → dataset vectorizado

  * `X`: vectores numéricos
  * `y`: categorías

---

## Integración con el proyecto

Este módulo proporciona:

* Datos listos para entrenamiento (`X`, `y`)
* Vocabulario compartido
* Función reutilizable `preprocess_text()`

Estos elementos son utilizados por:

* Persona 2 → entrenamiento del modelo
* Persona 3 → integración en la aplicación web

---

## Ejecución

Para ejecutar el pipeline:

```
python src/pipeline.py
```

---

## Requisitos

Instalar dependencias:

```
pip install -r requirements.txt
```

---

## Conclusión

El preprocesamiento transforma texto no estructurado en una representación numérica adecuada, lo cual es esencial para que el modelo de clasificación funcione correctamente. Esta etapa impacta directamente en el rendimiento y la calidad de las predicciones.
