from app.ai.whisper import load_whisper
# from app.ai.summarizer import load_summary_model
# from app.ai.rag import load_rag_model


class ModelManager:

    def __init__(self):

        self.whisper = None
        self.summarizer = None
        self.rag = None



    def load_models(self):

        print("Loading AI models...")


        self.whisper = load_whisper()

 
        # لاحقا
        # self.summarizer = load_summary_model()

        # self.rag = load_rag_model()


        print("All models loaded successfully")



model_manager = ModelManager()