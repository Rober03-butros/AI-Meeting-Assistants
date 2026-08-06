from transformers import AutoTokenizer
import os

TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), "model_tokenizer")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, local_files_only=True)