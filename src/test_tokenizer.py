from preprocessing.clean_text import clean_text
from preprocessing.tokenizer import tokenize

texto = "Question about cancelling order {{Order Number}}!!!"

limpio = clean_text(texto)
tokens = tokenize(limpio)

print("Texto limpio:", limpio)
print("Tokens:", tokens)