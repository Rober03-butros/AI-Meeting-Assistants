# from app.ai.whisper import load_whisper
from app.ai.embedding_model import load_embedding_model


class ModelManager:

    def __init__(self):

        self.whisper = None
        self.embedding_model = None



    def load_models(self):

        print("Loading AI models...")


        # self.whisper = load_whisper()
        self.embedding_model = load_embedding_model()

 
        # لاحقا
        # self.summarizer = load_summary_model()

        # self.rag = load_rag_model()


        print("All models loaded successfully")



model_manager = ModelManager()