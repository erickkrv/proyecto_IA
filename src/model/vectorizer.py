def build_vocab(textos_procesados):
    vocab = {}
    index = 0

    for tokens in textos_procesados:
        for palabra in tokens:
            if palabra not in vocab:
                vocab[palabra] = index
                index += 1

    return vocab


def text_to_bow(tokens, vocab):
    vector = [0] * len(vocab)

    for palabra in tokens:
        if palabra in vocab:
            vector[vocab[palabra]] += 1

    return vector