import math
import json

class NaiveBayesMultinomial:
    """
    Clasificador Naïve Bayes Multinomial construido desde cero.
    Especializado para texto vectorizado bajo Bag of Words.
    """
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # Parámetro de suavizado de Laplace
        self.classes = []
        self.prior_log_probs = {}
        self.cond_log_probs = {}
        self.vocab_size = 0

    def fit(self, X, y):
        """
        Entrena el modelo procesando las pre-frecuencias.
        X: lista de vectores (Bag of words, uno por documento)
        y: lista de categorías (etiquetas)
        """
        if not X or not y:
            raise ValueError("Las matrices X o y están vacías")

        # Contar documentos por clase
        class_counts = {}
        for cls in y:
            class_counts[cls] = class_counts.get(cls, 0) + 1
            
        self.classes = list(class_counts.keys())
        total_docs = len(y)
        
        self.vocab_size = len(X[0])
        
        # 1. Probabilidad a priori: log(P(clase))
        self.prior_log_probs = {
            cls: math.log(count / total_docs) for cls, count in class_counts.items()
        }
        
        # 2. Sumar cuenta de palabras por clase (acumulador)
        word_counts = {cls: [0] * self.vocab_size for cls in self.classes}
        
        for features, cls in zip(X, y):
            wc_cls = word_counts[cls]
            for i, freq in enumerate(features):
                if freq > 0:
                    wc_cls[i] += freq
                    
        # 3. Probabilidad condicional: log(P(palabra|clase)) con Laplace Smoothing
        self.cond_log_probs = {cls: [0.0] * self.vocab_size for cls in self.classes}
        
        for cls in self.classes:
            wc_cls = word_counts[cls]
            total_words_in_class = sum(wc_cls)
            # Denominador incluye + alpha * vocab_size (Laplace)
            denominator = total_words_in_class + (self.alpha * self.vocab_size)
            
            cond_log_cls = self.cond_log_probs[cls]
            for i in range(self.vocab_size):
                numerador = wc_cls[i] + self.alpha
                # Math.log en base e 
                cond_log_cls[i] = math.log(numerador / denominator)

    def predict(self, X):
        """
        Dado un vector o un de lista de vectores, retorna sus predicciones.
        Usa la suma de logaritmos enseñada para evitar underflow numérico.
        """
        predictions = []
        is_single = False
        
        if len(X) > 0 and isinstance(X[0], (int, float)):
            X = [X]
            is_single = True
            
        for features in X:
            best_prob = float("-inf")
            best_class = None
            
            for cls in self.classes:
                # La suma empieza con el log(base)
                prob_cls = self.prior_log_probs[cls]
                cond_log_cls = self.cond_log_probs[cls]
                
                for i, freq in enumerate(features):
                    if freq > 0:
                        # sumamos log(P(palabra|clase)) * cantidad de veces que sale
                        prob_cls += cond_log_cls[i] * freq
                        
                if prob_cls > best_prob:
                    best_prob = prob_cls
                    best_class = cls
                    
            predictions.append(best_class)
            
        if is_single:
            return predictions[0]
        return predictions

    def save(self, filepath):
        """
        Exporta el cerebro del modelo entrenado a texto plano JSON as requested for review.
        """
        model_data = {
            "alpha": self.alpha,
            "classes": self.classes,
            "vocab_size": self.vocab_size,
            "prior_log_probs": self.prior_log_probs,
            "cond_log_probs": self.cond_log_probs
        }
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(model_data, f, indent=4)
            
    def load(self, filepath):
        """
        Restaura el modelo sin tener que re-calcular log probabilidades.
        """
        with open(filepath, "r", encoding='utf-8') as f:
            model_data = json.load(f)
            self.alpha = model_data["alpha"]
            self.classes = model_data["classes"]
            self.vocab_size = model_data["vocab_size"]
            self.prior_log_probs = model_data["prior_log_probs"]
            self.cond_log_probs = model_data["cond_log_probs"]
