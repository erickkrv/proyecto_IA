from preprocessing.clean_text import clean_text
from preprocessing.tokenizer import tokenize
from model.vectorizer import build_vocab, text_to_bow

texto = "I want to cancel my order"

# Preprocesamiento
limpio = clean_text(texto)
tokens = tokenize(limpio)

# Crear vocabulario con solo este ejemplo
vocab = build_vocab([tokens])

# Convertir a vector
vector = text_to_bow(tokens, vocab)

print("Tokens:", tokens)
print("Vocabulario:", vocab)
print("Vector:", vector)