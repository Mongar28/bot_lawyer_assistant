from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def load_llm_openai(temperature=0.5, max_tokens=1000, model="gpt-4o-mini"):
    llm = ChatOpenAI(
        temperature=temperature,
        max_tokens=max_tokens,
        model=model,
    )
    return llm
