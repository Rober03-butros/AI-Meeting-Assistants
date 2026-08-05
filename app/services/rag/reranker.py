from app.ai.model_manager import model_manager
import numpy as np


def rerank_chunks(query: str,retrieved_chunks: list[dict],k: int = 5):

    reranker = model_manager.reranker_model

    if reranker is None:
        raise RuntimeError(
            "Reranker model is not loaded."
        )


    pairs = [
        (
            query,
            chunk["text"]
        )
        for chunk in retrieved_chunks
    ]


    scores = reranker.predict(pairs)


    sorted_indices = np.argsort(scores)[::-1]


    reranked_chunks = []


    for index in sorted_indices:

        chunk = retrieved_chunks[index]

        chunk["rerank_score"] = float(scores[index])

        reranked_chunks.append(chunk)


    return reranked_chunks[:k]