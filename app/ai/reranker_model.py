from sentence_transformers import CrossEncoder
# pip install sentence-transformers   


def load_reranker_model():

    print("Loading reranker model...")

    model = CrossEncoder("BAAI/bge-reranker-v2-m3")

    print("Reranker model loaded.")

    return model