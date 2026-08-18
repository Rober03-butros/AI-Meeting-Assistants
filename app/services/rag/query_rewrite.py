from app.ai.gemini import rewrite_query

def rewrite_question(question: str,conversation_history: str): 
    return rewrite_query(
        query=question,
        history=conversation_history,
    )