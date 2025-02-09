# Graph Definitions

- Los graphs con las abstracción centrales de `LangGraph`. Cada implementación de `StateGraph` es usada para crear un flujo de trabajo de grafos. Una vez compilado, usted puede correr el `CompiledGraph` para correr la aplicación.

# StateGraph

Es un gráfico cuyos nodos se comunican a través de un estado compartido. Esto significa que cada nodo puede leer y escribir información en un estado central que se utiliza para coordinar todo el flujo de trabajo.

```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class MyState(TypedDict)
    ...
    
graph = StateGraph(MyState)

```

### Firma de los nodos

Cada nodo del gráfico tiene la firma (función):

- **State -> Partial**: Significa que los nodos reciben el estado completo como entrada y generan un "estado parcial" como salida. El estado parcial es un subconjunto del estado completo que se utilizará o modificará por el nodo.

### Funciones Reducer

Cada clave del estado puede estar anotada opcionalmente con una **función reducer**. La función reducer se encarga de agregar o combinar los valores de esa clave cuando múltiples nodos intentan modificarla. La firma de esta función es:

- **(Value, Value) -> Value**: Combina dos valores en un solo valor, que es el resultado final después de la agregación.

```python
def reducer(a: list, b: int | None) -> list:
    if b is not None:
        return a + [b]
    return a

class State(TypedDict):
    x: Annotated[list, reducer]
```

### Parámetros:

1. **`state_schema`**: Define la clase que describe el esquema del estado. Aquí, es `MyState`, que indica qué estructura de datos se utilizará para almacenar el estado compartido.
2. **`config_schema`**: Es opcional y define la clase que describe el esquema de configuración. Se puede usar para exponer parámetros configurables en la API del gráfico.

### Aristas condicionales

El método `add_conditional_edges` permite agregar **aristas condicionales** a un grafo, conectando un nodo de origen con uno o varios nodos de destino, dependiendo de una condición. Una **arista condicional** es un camino que se sigue en función de una lógica definida en un nodo, permitiendo que el flujo del grafo se bifurque o cambie dinámicamente en base a decisiones. Aquí te explico cada parámetro y concepto clave:

### Parámetros:

1. **`source` (str)**:
    - Es el **nodo de origen**, el nodo desde el cual queremos que salga la arista condicional.
    - La ejecución del grafo alcanzará este nodo primero y, cuando lo abandone, se decidirá a qué nodo ir a continuación, basado en la condición proporcionada.
2. **`path` (Union[Callable, Runnable])**:
    - Es una función (`Callable`) o un (`Runnable`) que determina el siguiente nodo o nodos a los que debe dirigirse el flujo del grafo.
    - Este **`path`** puede devolver el nombre de uno o varios nodos de destino a los que el grafo debería ir a continuación.
    - **Si `path` devuelve `END`**, la ejecución del grafo terminará.
    - El resultado de esta función será evaluado para decidir qué nodo seguir a continuación.
3. **`path_map` (Optional[dict[Hashable, str]], default: None)**:
    - Es un **mapeo opcional** que asocia posibles valores de `path` con los nombres de los nodos a los que se debe dirigir el flujo del grafo.
    - Si no se proporciona, los resultados de `path` deben ser directamente los nombres de los nodos de destino. Si se proporciona, `path` puede devolver valores que luego se traducen a nombres de nodos a través de este diccionario.
4. **`then` (Optional[str], default: None)**:
    - Es el **nodo a ejecutar después** de que los nodos seleccionados por `path` terminen de ejecutarse.
    - Permite establecer un **nodo de continuación** al cual ir después de que se complete la rama de ejecución generada por `path`. Si no se especifica, el flujo continúa normalmente.

### Ejemplo conceptual

Supongamos que tienes un grafo de tres nodos: `A`, `B` y `C`. Queremos que, dependiendo de un valor de entrada, el grafo elija si va de `A` a `B` o de `A` a `C`.

```python
# Define the function that decides which node to go next based on input
def path_decider(state):
    if state["value"] > 10:
        return "B"
    else:
        return "C"

# Add a conditional edge
graph.add_conditional_edges(source="A", path=path_decider)
```

### Configurar el entry point

### `set_entry_point(key)`:

Este método se utiliza para establecer el **primer nodo** que se ejecutará en el grafo cuando se inicie el flujo de trabajo. Funciona de manera similar a agregar una arista que conecte un nodo especial, llamado **START**, con el nodo especificado por el parámetro `key`.

- **`key`**: Es una cadena de texto (`str`) que corresponde a la **clave** del nodo que se desea definir como punto de entrada (el primer nodo a ejecutar).
- **Equivalencia con `add_edge(START, key)`**: Internamente, este método establece una conexión directa entre un nodo de inicio implícito, llamado `START`, y el nodo especificado en `key`. Esto asegura que cuando se inicie la ejecución del grafo, el flujo comience por el nodo definido.
- **Retorno**: Devuelve el grafo en sí mismo (self) para permitir encadenar otros métodos si se desea.

### Ejemplo:

```python
graph.set_entry_point("Nodo_Inicial")
```

### `set_conditional_entry_point(path, path_map=None, then=None)`:

Este método establece un **punto de entrada condicional** en el grafo, lo que significa que la ejecución no comienza directamente en un nodo fijo, sino que depende de una condición o lógica especificada en el parámetro `path`.

- **`path (Union[Callable, Runnable])`**: Es un callable o runnable (como vimos anteriormente) que contiene la lógica para determinar el siguiente nodo o nodos a los que se dirigirá la ejecución. El `path` puede ser una función que, basándose en el estado o la configuración, decide qué nodo debe ejecutarse primero. Si el callable devuelve `END`, el grafo detendrá su ejecución.
- **`path_map (Optional[dict[str, str]], default: None)`**: Opcionalmente, puedes proporcionar un **mapeo** que asocie los valores de retorno de `path` con nombres de nodos. Por ejemplo, si `path` devuelve un valor como `"opción_1"`, `path_map` podría traducir `"opción_1"` a un nodo específico del grafo, como `"Nodo_A"`.
- **`then (Optional[str], default: None)`**: Este parámetro permite ejecutar un nodo específico **después** de que se haya seleccionado el nodo a través de `path`. Es útil si deseas garantizar que, después de que se haya determinado el nodo condicionalmente, se ejecute otro nodo en particular.
- **Retorno**: Devuelve el grafo en sí mismo (self) para permitir el encadenamiento de métodos.

### Ejemplo:

```python
def path_decision(state):
    if state["x"] > 10:
        return "Nodo_1"
    return "Nodo_2"

graph.set_conditional_entry_point(path=path_decision)
```

### `set_finish_point(key)`

Este método marca un nodo específico como **punto de finalización** del grafo. Cuando la ejecución del grafo alcanza este nodo, el flujo de ejecución se detiene. Es útil para definir cuándo el grafo ha completado su trabajo, ya que puede haber múltiples caminos posibles en el grafo, pero este nodo indica que se ha llegado al final.

- **Parámetro `key`**: Es una cadena de texto (`str`) que indica la **clave** o nombre del nodo que se desea definir como punto de finalización.
- **Comportamiento**: Cuando el grafo llega a este nodo, detiene su ejecución. Es un mecanismo para finalizar el flujo de trabajo.
- **Retorno**: Devuelve el grafo en sí mismo (`self`), permitiendo encadenar otros métodos si es necesario.

### Ejemplo:

```python
graph.set_finish_point("Nodo_Final")
```

Esto define que cuando la ejecución llegue al nodo llamado `"Nodo_Final"`, el grafo detendrá su ejecución.

### `add_node(node, action=None, ..., retry=None)`

Este método **añade un nuevo nodo** al grafo, el cual realizará una tarea específica. Los nodos son las unidades de trabajo en un grafo, y este método permite definir qué hace cada nodo.

- **`node (Union[str, RunnableLike])`**: Es el nombre del nodo o una función (`RunnableLike`) que define la lógica del nodo. Si es un nombre de cadena, ese será el identificador del nodo; si es una función, el nombre de la función se usará como nombre del nodo.
- **`action (Optional[RunnableLike], default: None)`**: (Opcional) Si se especifica, esta es la acción que realizará el nodo. Si no se especifica, el nodo ejecutará la acción correspondiente al valor de `node`.
- **`metadata (Optional[dict[str, Any]], default: None)`**: (Opcional) Metadatos asociados al nodo. Pueden ser cualquier información adicional que quieras asociar al nodo.
- **`input (Optional[Type[Any]], default: None)`**: (Opcional) El esquema de entrada que el nodo aceptará. Si no se proporciona, se utiliza el esquema de entrada predeterminado del grafo.
- **`retry (Optional[RetryPolicy], default: None)`**: (Opcional) Política de reintentos. Si se establece, define cómo y cuándo el nodo debería reintentarse si ocurre un error.
- **`Raises`**: Si el nombre o clave de este nodo ya está siendo utilizado en otro nodo del estado, lanzará un `ValueError`.

### Ejemplo 1: Añadir un nodo con nombre automático

```python
from langgraph.graph import START, StateGraph

builder = StateGraph(dict)
builder.add_node(my_node)  # El nodo se llamará 'my_node' automáticamente
builder.add_edge(START, "my_node")
graph = builder.compile()
resultado = graph.invoke({"x": 1})
print(resultado)
# {'x': 2}
```

En este ejemplo:

- Se define un nodo que incrementa el valor de `x` en el estado.
- El nombre del nodo será `my_node` (por el nombre de la función).
- Se conecta el nodo `START` con `my_node` y se invoca el grafo con un estado inicial `{ "x": 1 }`.

### Ejemplo 2: Añadir un nodo con un nombre personalizado

```python
builder = StateGraph(dict)
builder.add_node("mi_nodo_personalizado", my_node)  # Personaliza el nombre del nodo
builder.add_edge(START, "mi_nodo_personalizado")
graph = builder.compile()
resultado = graph.invoke({"x": 1})
print(resultado)
# {'x': 2}
```

Aquí, el nodo se llama `"mi_nodo_personalizado"`, pero ejecuta la misma función `my_node`.

### **`add_edge(start_key, end_key)`**

Esta función agrega una **conexión dirigida** entre dos nodos en un grafo. Es decir, crea un **camino** que el flujo seguirá de manera automática desde el nodo de inicio (**`start_key`**) hasta el nodo de destino (**`end_key`**).

### **Parámetros**:

1. **`start_key`** (Union[str, list[str]]):
    
    Este parámetro indica el **nodo de inicio** de la conexión. Puede ser:
    
    - Una **cadena de texto** (un único nodo de inicio).
    - Una **lista de cadenas** (varios nodos de inicio). En este caso, cada uno de los nodos de la lista estará conectado al mismo nodo de destino.
2. **`end_key`** (str):
    
    Este parámetro indica el **nodo de destino** de la conexión. Es una cadena de texto que representa el nombre del nodo al cual el flujo debe dirigirse después de pasar por el nodo de inicio.
    

### **¿Qué sucede cuando se llama a `add_edge(start_key, end_key)`?**

- Cuando el flujo del grafo llega a `start_key`, **automáticamente** se mueve al nodo indicado por `end_key`.
- Si `start_key` es una lista, se establece una conexión para cada nodo de esa lista hacia el nodo de destino (`end_key`).

### **Ejemplos de uso**:

1. **Agregar una conexión entre dos nodos:**
    
    Si tienes un grafo con dos nodos, `"A"` y `"B"`, y quieres que cuando el flujo llegue al nodo `"A"`, automáticamente pase al nodo `"B"`, se usa así:
    
    ```python
    graph.add_edge("A", "B")
    ```
    
    - En este caso, cuando el flujo llegue a `"A"`, inmediatamente se moverá a `"B"`.
2. **Agregar una conexión desde múltiples nodos a un único nodo:**
    
    Si tienes varios nodos de inicio, como `"A"` y `"C"`, y quieres que ambos se conecten al nodo `"B"`, se usa una lista para el parámetro `start_key`:
    
    ```python
    graph.add_edge(["A", "C"], "B")
    ```
    
    Aquí, tanto el nodo `"A"` como el nodo `"C"` se conectan a `"B"`. Si el flujo llega a `"A"` o `"C"`, en ambos casos pasará a `"B"`.
    

### **Excepciones**:

- **`ValueError`**: Se lanzará si intentas:
    1. Usar el nodo `END` como nodo de inicio (`start_key`). Esto es porque `END` indica el final del grafo, y no puede tener conexiones salientes.
    2. Usar un nodo (`start_key` o `end_key`) que **no existe** en el grafo.

### **Función `create_react_agent`**

La función `create_react_agent` crea un grafo que permite a un modelo de lenguaje en LangChain interactuar con herramientas. Este grafo es útil para manejar flujos de conversación y ejecutar acciones basadas en las entradas del usuario.

### **Parámetros:**

1. **`model (BaseChatModel)`**:
    - Es el modelo de lenguaje de LangChain que soporta la llamada a herramientas.
2. **`tools (Union[ToolExecutor, Sequence[BaseTool], ToolNode])`**:
    - Una lista de herramientas que el modelo puede utilizar. Puede ser una lista de herramientas (`BaseTool`), un ejecutor de herramientas (`ToolExecutor`), o un nodo de herramienta (`ToolNode`).
3. **`state_schema (Optional[StateSchemaType], default: None)`**:
    - Define el esquema del estado del grafo. Debe incluir `messages` (los mensajes del chat) y `is_last_step` (si es el último paso). Si no se define, se usa el estado por defecto.
4. **`messages_modifier (Optional[MessagesModifier], default: None)`**:
    - Modifica los mensajes **antes** de enviarlos al modelo de lenguaje.
    - Formas posibles:
        - `SystemMessage`: Añade un mensaje al principio de la lista.
        - `str`: Se convierte en un `SystemMessage` y se añade al principio.
        - `Callable`: Función que toma una lista de mensajes y los ajusta antes de pasarlos al modelo.
    - **Nota**: Este parámetro será eliminado en la versión 0.2.0.
5. **`state_modifier (Optional[StateModifier], default: None)`**:
    - Modifica el estado completo del grafo antes de enviarlo al modelo de lenguaje.
    - Formas posibles:
        - `SystemMessage`, `str`, `Callable`.
6. **`checkpointer (Checkpointer, default: None)`**:
    - Objeto opcional para guardar puntos de control del estado del chat.
7. **`interrupt_before (Optional[list[str]], default: None)`**:
    - Lista opcional de nodos donde interrumpir **antes** de ejecutar. Ej: `"agent"` o `"tools"`.
8. **`interrupt_after (Optional[list[str]], default: None)`**:
    - Similar a `interrupt_before`, pero interrumpe **después** de que el nodo termine la acción.
9. **`debug (bool, default: False)`**:
    - Activa o desactiva el modo de depuración para ver más detalles del proceso.

### **Retorno:**

- Devuelve un **`CompiledGraph`**: Un grafo compilado que puede ser utilizado en interacciones de chat y que maneja tanto la conversación como la ejecución de herramientas

![image.png](Graph%20Definitions%20d375f0ef634d4920b072ed83b325472d/image.png)

- **Nodo "agent"**:
    - Llama al modelo de lenguaje con la lista de mensajes.
    - Si el mensaje resultante (`AIMessage`) incluye **tool_calls**, el grafo procede a invocar las herramientas.
- **Nodo "tools"**:
    - Ejecuta las herramientas, una por cada **tool_call**.
    - Las respuestas de las herramientas se agregan a la lista de mensajes como objetos `ToolMessage`.
- **Repetición del proceso**:
    - El nodo "agent" vuelve a llamar al modelo de lenguaje con la nueva lista de mensajes, que ahora incluye las respuestas de las herramientas.
    - El proceso se repite hasta que no haya más **tool_calls** en la respuesta del modelo.
- **Resultado final**:
    - El nodo "agent" devuelve la lista completa de mensajes como un diccionario que contiene la clave `"messages"`

### **Ejemplo de uso con una herramienta simple**

1. **Importaciones y definición de la herramienta:**
    - Se importa `datetime`, el decorador `tool` de LangChain, y se configura el modelo `ChatOpenAI` para usar en el grafo.
    - Se define una herramienta llamada `check_weather` que simula devolver el pronóstico del clima para una ubicación específica.
    
    ```python
    from datetime import datetime
    from langchain_core.tools import tool
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent
    
    @tool
    def check_weather(location: str, at_time: datetime | None = None) -> float:
        '''Return the weather forecast for the specified location.'''
        return f"It's always sunny in {location}"
    ```
    
2. **Configuración del grafo:**
    - Se crea una lista con la herramienta `check_weather`.
    - Se configura el modelo de lenguaje con `gpt-4o-mini`.
    - Se construye el grafo usando la función `create_react_agent`.
    
    ```python
    tools = [check_weather]
    model = ChatOpenAI(model="gpt-4o-mini")
    graph = create_react_agent(model, tools=tools)
    ```
    
3. **Ejemplo de interacción:**
    - El grafo procesa la entrada, ejecuta la herramienta, y genera respuestas en cada iteración del ciclo.
    - Se crea un mensaje de entrada del usuario preguntando por el clima en San Francisco (`sf`).
    
    ```python
    inputs = {"messages": [("user", "Cual es el clima en Bogota?")]}
    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
    ```
    
    Otra forma de generar una respuesta:
    
    ```python
    inputs = {"messages": [("user", "Cual es el clima en Bogota?")]}
    response = graph.invoke(inputs)
    
    print(response["messages"][-1].content)
    ```
    

### **Agregar un prompt de sistema para el modelo de lenguaje:**

1. **Definición del prompt de sistema:**
    - Se agrega un mensaje de sistema que le dice al modelo que debe actuar como un bot llamado Fred.
    
    ```python
    system_prompt = "You are a helpful bot named Fred."
    graph = create_react_agent(model, tools, state_modifier=system_prompt)
    ```
    

### **Agregar un prompt más complejo para el modelo de lenguaje (LLM)**

1. **Importación y definición del prompt:**
    - Se utiliza `ChatPromptTemplate` para definir un prompt personalizado. Este prompt incluye varios tipos de mensajes: un mensaje de sistema, un marcador de posición para los mensajes, y un recordatorio del usuario para que el bot sea siempre educado.
    
    ```python
    from langchain_core.prompts import ChatPromptTemplate
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful bot named Fred."),
        ("placeholder", "{messages}"),
        ("user", "Remember, always be polite!"),
    ])
    ```
    
2. **Modificación del estado de los mensajes:**
    - Se define una función `modify_state_messages` que recibe el estado del agente (`AgentState`).
    - En esta función, se realiza una invocación del prompt con los mensajes actuales, lo que permite hacer modificaciones complejas en el estado antes de pasarlo al modelo.

```python
def modify_state_messages(state: AgentState):
    # Puedes realizar modificaciones más complejas aquí
    return prompt.invoke({"messages": state["messages"]})
```

1. **Configuración del grafo con el nuevo state_modifier:**
- Se construye el grafo utilizando `create_react_agent`, pasando tanto el modelo como las herramientas, además del `state_modifier` que utiliza la función `modify_state_messages`.

```python
graph = create_react_agent(model, tools, state_modifier=modify_state_messages)
```

1. **Interacción con el grafo:**
- Se envían los mensajes de entrada para preguntar el nombre del bot y el clima en San Francisco, y se procesa la salida utilizando `graph.stream` para obtener los resultados paso a paso

```python
inputs = {"messages": [("user", "What's your name? And what's the weather in SF?")]}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()
```

### **Prompt complejo con estado de grafo personalizado**

1. **Importación y definición del prompt:**
    - Se crea un `ChatPromptTemplate` que incluye un mensaje del sistema que inserta la fecha actual y un marcador de posición para los mensajes del usuario.

```python
from typing import TypedDict
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Today is {today}"),
        ("placeholder", "{messages}"),
    ]
)
```

1. **Definición del estado personalizado (`CustomState`):**
    - Se define una clase personalizada que extiende `TypedDict` para almacenar el estado del grafo. Este estado incluye:
        - `today`: una cadena con la fecha actual.
        - `messages`: una lista anotada con `BaseMessage` y una función `add_messages`.
        - `is_last_step`: un indicador de si es el último paso en el flujo de la conversación.

```python
class CustomState(TypedDict):
    today: str
    messages: Annotated[list[BaseMessage], add_messages]
    is_last_step: str
```

1. **Configuración del grafo con el estado personalizado:**
    - Se construye el grafo utilizando `create_react_agent`, pasando el modelo, las herramientas, y el esquema del estado personalizado (`state_schema`) junto con el `state_modifier` que utiliza el prompt definido.

```python
graph = create_react_agent(model, tools, state_schema=CustomState, state_modifier=prompt)
```

1. **Interacción con el grafo:**
    - Se envían los mensajes de entrada que preguntan la fecha de hoy y el clima en San Francisco. Se incluye la fecha específica como parte del estado en el input. El grafo procesa la salida utilizando `graph.stream`.

```python
inputs = {"messages": [("user", "What's today's date? And what's the weather in SF?")], "today": "July 16, 2004"}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()
```