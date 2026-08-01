from sentence_transformers import SentenceTransformer
# pip install sentence-transformers   


def load_embedding_model():

    print("Loading embedding model...")

    model = SentenceTransformer(
        "BAAI/bge-m3"
    )

    print("Embedding model loaded.")

    return model