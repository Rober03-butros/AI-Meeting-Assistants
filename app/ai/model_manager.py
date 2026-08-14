from app.ai.whisper import load_whisper
from app.ai.embedding_model import load_embedding_model
from app.ai.reranker_model import load_reranker_model


class ModelManager:

    def __init__(self):

        self.whisper = None
        self.embedding_model = None
        self.reranker_model = None



    def load_models(self):

        print("Loading AI models...")


        self.whisper = load_whisper()
        self.embedding_model = load_embedding_model()
        self.reranker_model = load_reranker_model()




        print("All models loaded successfully")



model_manager = ModelManager()