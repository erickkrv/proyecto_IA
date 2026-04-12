from preprocessing.clean_text import clean_text

texto = "Question about cancelling order {{Order Number}}!!!"

resultado = clean_text(texto)

print("Original:", texto)
print("Limpio:", resultado)