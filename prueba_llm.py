from langgraph_components.llm import load_llm_deepseek, load_llm_openai

llm = load_llm_deepseek()
print(llm.invoke("hello"))

llm_2 = load_llm_openai()
print(llm_2.invoke("hello"))