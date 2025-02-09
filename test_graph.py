from langgraph_components.graph import load_graph

def test_graph_response():
    # Cargar el grafo
    graph = load_graph()
    
    # Configuración de prueba
    config = {"configurable": {"thread_id": "thread-1", "recursion_limit": 50}}
    test_input = "Hola"
    
    # Estado inicial
    initial_state = {
        "messages": [{"role": "user", "content": test_input}],
        "remaining_steps": 10
    }
    
    print("\nEnviando mensaje de prueba:", test_input)
    print("\nEstructura del estado inicial:", initial_state)
    
    # Obtener eventos
    events = graph.stream(initial_state, config, stream_mode="updates")
    
    print("\nProcesando eventos:")
    for event in events:
        print("\nEvento completo:", event)
        if "agent" in event:
            print("\nMensajes del agente:", event["agent"]["messages"])
            print("\nÚltimo mensaje:", event["agent"]["messages"][-1])
            print("\nTipo del último mensaje:", type(event["agent"]["messages"][-1]))
            
            # Intentar diferentes formas de acceder al contenido
            message = event["agent"]["messages"][-1]
            print("\nAtributos del mensaje:", dir(message))
            
            if hasattr(message, 'content'):
                print("\nContenido a través de .content:", message.content)
            
            try:
                print("\nContenido a través de ['content']:", message['content'])
            except:
                print("\nNo se puede acceder como diccionario")
            
            print("\nRepresentación como string:", str(message))

if __name__ == "__main__":
    test_graph_response()