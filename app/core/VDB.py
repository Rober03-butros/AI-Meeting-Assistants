import faiss
import numpy as np
from pathlib import Path


VECTOR_FOLDER = Path(
    "storage/vectors"
)


VECTOR_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)


def build_faiss_index(embeddings: np.ndarray):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings.astype("float32")
    )

    return index

def save_faiss_index(meeting_id: int,index):

    path = (
        VECTOR_FOLDER /
        f"meeting_{meeting_id}.index"
    )

    faiss.write_index(
        index,
        str(path),
    )



def load_faiss_index(meeting_id: int):

    path = (
        VECTOR_FOLDER /
        f"meeting_{meeting_id}.index"
    )


    if not path.exists():

        raise FileNotFoundError(
            "FAISS index not found"
        )


    return faiss.read_index(
        str(path)
    )

