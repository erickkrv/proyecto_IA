from datasets import load_dataset

def cargar_dataset():
    dataset = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")
    data = dataset["train"]

    textos = [x["instruction"] for x in data]
    categorias = [x["category"] for x in data]

    return textos, categorias