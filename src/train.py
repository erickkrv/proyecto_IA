import json
import os
from evaluation.k_folds import evaluate_k_folds
from model.naive_bayes import NaiveBayesMultinomial

def main():
    dataset_path = "results/dataset_vectorizado.json"
    
    if not os.path.exists(dataset_path):
        print(f"[ERROR] No se encontró el archivo: {dataset_path}")
        print("Asegúrate de que la Persona 1 ejecutó 'src/pipeline.py' correctamente antes.")
        return
        
    print(f"[INFO] Cargando dataset desde {dataset_path}...")
    with open(dataset_path, "r", encoding='utf-8') as f:
        data = json.load(f)
        
    X = data["X"]
    y = data["y"]
    
    print(f"[INFO] Cargados exitosamente {len(X)} documentos con representaciones vectorizadas.")
    
    # ==============================================================
    # 1. VALIDACIÓN RIGUROSA (K-FOLDS) - EXIGENCIA ACADÉMICA
    # ==============================================================
    evaluate_k_folds(X, y, k=5)
    
    # ==============================================================
    # 2. ENTRENAMIENTO FINAL (100% DATASET) - EXIGENCIA PRODUCCIÓN
    # ==============================================================
    print("\n[INFO] Entrenando modelo final definitivo con el 100% de las instancias...")
    final_model = NaiveBayesMultinomial(alpha=1.0)
    final_model.fit(X, y)
    
    # ==============================================================
    # 3. PERSISTENCIA (GUARDADO EN JSON PLANO PARA LA DEFENSA)
    # ==============================================================
    os.makedirs("models", exist_ok=True)
    model_save_path = "models/naive_bayes_model.json"
    final_model.save(model_save_path)
    
    print(f"\n[ÉXITO] Modelo de IA exportado satisfactoriamente hacia: {model_save_path}")


if __name__ == "__main__":
    main()
