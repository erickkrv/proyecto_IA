import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# descargar stopwords (solo la primera vez)
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def tokenize(texto):
    tokens = texto.split()

    # eliminar stopwords
    tokens = [t for t in tokens if t not in stop_words]

    # aplicar stemming
    tokens = [stemmer.stem(t) for t in tokens]

    return tokens