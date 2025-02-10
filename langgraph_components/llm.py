from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm_openai(temperature=0.5, max_tokens=1000, model="gpt-4o-mini"):
    llm = ChatOpenAI(
        temperature=temperature,
        max_tokens=max_tokens,
        model=model,
    )
    return llm

def load_llm_deepseek(temperature=0.5, max_tokens=1000, model="deepseek-chat"):
    llm = ChatOpenAI(
        temperature=temperature,
        max_tokens=max_tokens,
        model=model,
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    return llm