from langchain_groq import ChatGroq

def get_llm(is_temp: bool = False):
    if is_temp:
        return ChatGroq(model_name="openai/gpt-oss-20b", temperature=0.5)
    else:
        return ChatGroq(model_name='meta-llama/llama-4-scout-17b-16e-instruct')