from dotenv import load_dotenv
from langgraph_components.states import State
from langgraph_components.graph import load_graph
import streamlit as st
import re

def validate_email(email: str) -> bool:
    """Valida que el email tenga un formato correcto"""
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(email_pattern.match(email))

def initialize_session_state():
    """Inicializa el estado de la sesión si no existe"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "email" not in st.session_state:
        st.session_state.email = None
    if "current_state" not in st.session_state:
        st.session_state.current_state = None
    if "graph" not in st.session_state:
        load_dotenv()
        st.session_state.graph = load_graph()
    if "waiting_for_response" not in st.session_state:
        st.session_state.waiting_for_response = False

def main():
    st.markdown("<h1 style='text-align: center;'>Temis - Asistente Legal Virtual</h1>", 
                unsafe_allow_html=True)
    
    # Inicializar estado de sesión
    initialize_session_state()
    
    # Solicitar email en el sidebar
    email = st.sidebar.text_input(
        "Ingresa tu correo electrónico:",
        value=st.session_state.email if st.session_state.email else "",
        key="email_input"
    )
    
    # Validar email
    if email:
        if validate_email(email):
            st.session_state.email = email
            if st.session_state.current_state is None:
                st.session_state.current_state = State(
                    messages=[], 
                    remaining_steps=3
                )
        else:
            st.sidebar.error("Correo electrónico inválido. Por favor, verifica el formato.")
            return

    # Si no hay email válido, no mostrar el chat
    if not st.session_state.email:
        st.info("Por favor, ingresa un correo electrónico válido para comenzar.")
        return

    # Mostrar historial de mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    user_input = st.chat_input("¿En qué puedo ayudarte hoy?")
    
    if user_input and st.session_state.current_state:
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.waiting_for_response = True
        
        # Mostrar el mensaje del usuario
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Mostrar indicador de carga mientras se procesa la respuesta
        with st.chat_message("assistant"):
            with st.spinner("Generando respuesta..."):
                try:
                    # Configurar el estado inicial y config para el stream
                    config = {"configurable": {"thread_id": "thread-1", "recursion_limit": 50}}
                    initial_state = {
                        "messages": [{"role": "user", "content": user_input}],
                        "remaining_steps": 10
                    }
                    
                    # Obtener el stream de eventos
                    events = st.session_state.graph.stream(
                        initial_state,
                        config,
                        stream_mode="updates"
                    )

                    # Procesar los eventos
                    for event in events:
                        if "agent" in event:
                            # Obtener el mensaje del asistente (AIMessage)
                            ai_message = event["agent"]["messages"][-1]
                            response = ai_message.content
                            
                            # Agregar respuesta al historial
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": response
                            })
                            st.markdown(response)
                            
                            # Actualizar el estado actual
                            if st.session_state.current_state is None:
                                st.session_state.current_state = State(
                                    messages=st.session_state.messages.copy(),
                                    remaining_steps=10
                                )
                            else:
                                st.session_state.current_state["messages"] = st.session_state.messages.copy()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                
                st.session_state.waiting_for_response = False

if __name__ == "__main__":
    main()