import streamlit as st
import time
# Importamos todas las funciones desde applaberinto
from applaberinto import MAZE, START, END, solve_maze_bfs, solve_maze_dfs, solve_maze_astar

st.set_page_config(page_title="Maze Solver Pro", page_icon="🧩", layout="wide")

st.title("Visualizador de Algoritmo de Búsqueda")
st.write("Comparación de algoritmos en un laberinto complejo.")

# Función para renderizar el laberinto
def render_maze(maze, path=None):
    if path is None:
        path = []
    
    path_set = set(path) # Convertir a set para búsqueda O(1) rápida
    
    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            if (r_idx, c_idx) == START:
                display_row.append("🟢") 
            elif (r_idx, c_idx) == END:
                display_row.append("🏁") 
            elif (r_idx, c_idx) in path_set:
                display_row.append("🟦") 
            elif col == 1:
                display_row.append("⬛") 
            else:
                display_row.append("⬜") 
        display_maze.append("".join(display_row))
    
    # Ajustamos el tamaño de fuente más pequeño porque el laberinto es grande
    st.markdown(
        f"""
        <div style="font-family: monospace; line-height: 1.0; font-size: 10px; white-space: pre;">
            {'<br>'.join(display_maze)}
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- Sidebar ---
st.sidebar.header("Configuración")
algorithm = st.sidebar.selectbox(
    "Selecciona el algoritmo", 
    ["BFS (Búsqueda en Amplitud)", "DFS (Búsqueda en Profundidad)", "A* (A-Star)"]
)
solve_button = st.sidebar.button("Resolver Laberinto")

# --- Lógica ---
col1, col2 = st.columns([3, 1])

with col1:
    if not solve_button:
        st.subheader("Laberinto Inicial")
        render_maze(MAZE)

    if solve_button:
        path = None
        st.subheader(f"Resultado: {algorithm}")
        
        start_time = time.perf_counter()
        
        if "BFS" in algorithm:
            path = solve_maze_bfs(MAZE, START, END)
        elif "DFS" in algorithm:
            path = solve_maze_dfs(MAZE, START, END)
        elif "A*" in algorithm:
            path = solve_maze_astar(MAZE, START, END)
            
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000 

        if path:
            render_maze(MAZE, path)
            st.success(f"¡Meta alcanzada!")
        else:
            st.error("No se encontró salida.")
            render_maze(MAZE)

with col2:
    if solve_button and path:
        st.metric(label="Tiempo de Ejecución", value=f"{elapsed_time:.4f} ms")
        st.metric(label="Pasos en el camino", value=f"{len(path)}")
        
        st.info("""
        **Nota sobre los algoritmos:**
        * **BFS:** Encuentra el camino más corto garantizado.
        * **DFS:** Puede encontrar caminos muy largos y dar muchas vueltas, pero usa menos memoria.
        * **A*:** Encuentra el camino más corto (igual que BFS) pero usualmente mucho más rápido porque sabe a dónde ir.
        """)
