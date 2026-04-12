import random
from model.naive_bayes import NaiveBayesMultinomial
from evaluation.metrics import (
    calculate_accuracy, 
    calculate_precision_recall_f1, 
    calculate_macro_f1, 
    build_confusion_matrix, 
    print_confusion_matrix, 
    print_metrics_report
)

def k_folds_split(X, y, k=5, seed=42):
    """
    Divide el dataset en K particiones de forma aleatoria, 
    devolviendo una lista de particiones.
    """
    random.seed(seed)
    dataset = list(zip(X, y))
    random.shuffle(dataset)
    
    fold_size = len(dataset) // k
    folds = []
    
    for i in range(k):
        start = i * fold_size
        # El último fold se lleva el residuo posible si no es exacto
        end = (i + 1) * fold_size if i != k - 1 else len(dataset)
        folds.append(dataset[start:end])
        
    return folds

def evaluate_k_folds(X, y, k=5):
    """
    Realiza la validación cruzada y emite el reporte de métricas y la matriz de confusión.
    Retorna el promedio de accuracy.
    """
    print(f"\n[INFO] Ejecutando {k}-Folds Cross Validation...")
    folds = k_folds_split(X, y, k)
    
    fold_accuracies = []
    global_y_true = []
    global_y_pred = []
    
    for i in range(k):
        print(f" -> Evaluando Fold {i+1}/{k}...")
        
        # Test es el fold actual
        val_data = folds[i]
        # Train es el resto
        train_data = []
        for j in range(k):
            if i != j:
                train_data.extend(folds[j])
                
        # Separamos nuevamente en X y y
        X_train, y_train = zip(*train_data)
        X_val, y_val = zip(*val_data)
        
        # Instanciar el modelo (cerebro)
        model = NaiveBayesMultinomial(alpha=1.0)
        
        # Entrenar
        model.fit(X_train, y_train)
        
        # Predecir
        predictions = model.predict(X_val)
        
        # Acumular registros
        global_y_true.extend(y_val)
        global_y_pred.extend(predictions)
        
        # Métricas individuales de cada fold
        acc = calculate_accuracy(y_val, predictions)
        fold_accuracies.append(acc)
        
    # Análisis de varianza (requerido por el documento)
    varianza = sum((x - (sum(fold_accuracies)/k))**2 for x in fold_accuracies) / k
    dif_max_min = max(fold_accuracies) - min(fold_accuracies)
    
    print("\n--- RESULTADOS K-FOLDS ---")
    print(f"Accuracies obtenidas : {[round(a, 4) for a in fold_accuracies]}")
    print(f"Promedio general     : {sum(fold_accuracies)/k:.4f}")
    print(f"Varianza de Folds    : {varianza:.6f}")
    print(f"Diferencia (Max-Min) : {dif_max_min:.4f}")
    
    # Ahora que tenemos 1 predict por cada dato (fuera de muestra), sacamos el macro completo.
    final_acc = calculate_accuracy(global_y_true, global_y_pred)
    class_metrics = calculate_precision_recall_f1(global_y_true, global_y_pred)
    macro_f1 = calculate_macro_f1(class_metrics)
    
    print_metrics_report(final_acc, class_metrics, macro_f1)
    
    conf_matrix, classes = build_confusion_matrix(global_y_true, global_y_pred)
    print_confusion_matrix(conf_matrix, classes)
