from .llm import load_llm_openai
from .graph_tools import tools
from langchain_core.prompts import ChatPromptTemplate
from langgraph_components.states import State
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
import yaml


# Cargar prompts
def load_config():
    with open("config/prompts.yaml", "r") as file:
        return yaml.safe_load(file)


def load_graph():
    prompts = load_config()
    llm = load_llm_openai()

    # Configurar el prompt del sistema
    system_prompt = ChatPromptTemplate.from_messages([
        ("system", prompts["prompt_assistant"]),
        ("placeholder", "{messages}")
    ])

    # Crear el graph con el estado definido
    graph = create_react_agent(
        model=llm,
        tools=tools,
        state_schema=State,
        state_modifier=system_prompt,
        checkpointer=MemorySaver(),
    )

    return graph

# graph = load_graph()

# print("Bienvenido al asistente virtual de abogado Saul")
# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Adios!")
#         break
        
#     config = {"configurable": {"thread_id": "thread-1", "recursion_limit": 50}}
#     events = graph.stream(
#         {
#             "messages": [{"role": "user", "content": user_input}],
#             "remaining_steps": 10
#         },
#         config,
#         stream_mode="updates"
#     )

#     for event in events:
#         if "agent" in event:
#             response = event["agent"]["messages"][-1].content
#             print(f"\nAsistente: {response}\n")