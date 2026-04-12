def calculate_accuracy(y_true, y_pred):
    """ Calcula la exactitud total del modelo (Accuracy global). """
    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    return correct / len(y_true) if len(y_true) > 0 else 0.0

def calculate_precision_recall_f1(y_true, y_pred):
    """
    Calcula Precision, Recall y F1-Score para cada clase.
    Retorna un diccionario: { "CLASE": {"precision": p, "recall": r, "f1": f1} }
    """
    classes = set(y_true) | set(y_pred)
    metrics = {}
    
    for cls in classes:
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == cls and yp == cls)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt != cls and yp == cls)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == cls and yp != cls)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        metrics[cls] = {
            "precision": precision,
            "recall": recall,
            "f1": f1
        }
        
    return metrics

def calculate_macro_f1(metrics_por_clase):
    """
    Calcula el Macro F1 promediando los F1 scores de todas las clases.
    """
    if not metrics_por_clase:
        return 0.0
    
    total_f1 = sum(m["f1"] for m in metrics_por_clase.values())
    return total_f1 / len(metrics_por_clase)

def build_confusion_matrix(y_true, y_pred):
    """
    Crea una matriz de confusión en forma de diccionario de diccionarios.
    matrix[true_class][predicted_class] = count
    """
    classes = sorted(list(set(y_true) | set(y_pred)))
    matrix = {c: {c_pred: 0 for c_pred in classes} for c in classes}
    
    for yt, yp in zip(y_true, y_pred):
        matrix[yt][yp] += 1
        
    return matrix, classes

def print_metrics_report(accuracy, class_metrics, macro_f1):
    """ Imprime el reporte ordenado en la terminal """
    print(f"\n--- REPORTE DE MÉTRICAS ---")
    print(f"Accuracy Global : {accuracy:.4f}")
    print(f"Macro F1-Score  : {macro_f1:.4f}\n")
    
    print(f"{'Clase':<20} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 58)
    for cls, m in sorted(class_metrics.items()):
        print(f"{cls:<20} | {m['precision']:<10.4f} | {m['recall']:<10.4f} | {m['f1']:<10.4f}")
    print("-" * 58)

def print_confusion_matrix(matrix, classes):
    """
    Imprime la matriz de confusión visualmente ordenando las clases en filas (Real) y columnas (Predicción).
    """
    print("\n--- MATRIZ DE CONFUSIÓN ---")
    print("Filas = Real, Columnas = Predicción\n")
    
    # Reducimos los nombres a 8 letras para que quepa en la pantalla
    short_classes = [c[:8] for c in classes]
    headers = "".join([f"{c:>9}" for c in short_classes])
    print(f"{'Real/Pred':<12} {headers}")
    print("-" * (13 + 9 * len(classes)))
    
    for yt in classes:
        row_str = f"{yt[:10]:<12} |"
        for yp in classes:
            count = matrix[yt][yp]
            # Si el valor es cero se muestra difuminado o con un 0 para identificar facil
            row_str += f"{count:>8} "
        print(row_str)
