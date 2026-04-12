from utils.load_data import cargar_dataset

textos, categorias = cargar_dataset()

print("Primer texto:", textos[0])
print("Primera categoría:", categorias[0])
print("Total datos:", len(textos))