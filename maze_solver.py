import streamlit as st
import time
# Importamos la lógica y los datos desde applaberinto
from applaberinto import MAZE, START, END, solve_maze_bfs, solve_maze_dfs, solve_maze_astar

st.set_page_config(page_title="Maze Solver - 3 Métodos", layout="wide")

st.title("🧩 Solucionador de Laberintos")
st.markdown("Comparación de algoritmos: **BFS**, **DFS** y **A***")

# --- Función de Visualización ---
def render_maze(maze, path=None):
    if path is None:
        path = []
    path_set = set(path) # Optimización para búsqueda rápida
    
    rows = len(maze)
    cols = len(maze[0])
    
    html_maze = []
    
    # Renderizamos fila por fila
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            cell_value = maze[r][c]
            
            # Definimos el símbolo a dibujar
            if (r, c) == START:
                symbol = "🟢" # Inicio
            elif (r, c) == END:
                symbol = "🏁" # Fin
            elif (r, c) in path_set:
                symbol = "🟦" # Camino
            elif cell_value == 1:
                symbol = "⬛" # Muro
            else:
                symbol = "⬜" # Pasillo libre
            
            row_str += symbol
        html_maze.append(row_str)
    
    # CSS para forzar que los caracteres se vean cuadrados y alineados
    # Usamos line-height ajustado y una fuente monoespaciada
    st.markdown(
        f"""
        <div style="
            font-family: 'Courier New', monospace; 
            line-height: 0.8; 
            font-size: 14px; 
            letter-spacing: 0px;
            white-space: pre; 
            overflow-x: auto;
            border: 2px solid #333;
            display: inline-block;
            padding: 10px;
            background-color: #f0f0f0;
        ">
            {'<br>'.join(html_maze)}
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- Sidebar (Barra Lateral) ---
st.sidebar.header("Configuración")

# Información del Mapa
st.sidebar.info(f"Dimensiones: {len(MAZE)}x{len(MAZE[0])}")
st.sidebar.text(f"Inicio: {START}")
st.sidebar.text(f"Meta: {END}")

# Selector de Algoritmo
algo_option = st.sidebar.radio(
    "Selecciona el Algoritmo:",
    ("BFS (Amplitud)", "DFS (Profundidad)", "A* (A-Star)")
)

solve_btn = st.sidebar.button("🚀 Resolver Laberinto", type="primary")

# --- Lógica Principal ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Visualización del Laberinto")
    if not solve_btn:
        # Mostrar estado inicial
        render_maze(MAZE)
    else:
        # Resolver
        path = None
        start_time = time.perf_counter()
        
        try:
            if "BFS" in algo_option:
                path = solve_maze_bfs(MAZE, START, END)
            elif "DFS" in algo_option:
                path = solve_maze_dfs(MAZE, START, END)
            elif "A*" in algo_option:
                path = solve_maze_astar(MAZE, START, END)
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        if path:
            render_maze(MAZE, path)
            st.success("¡Camino encontrado con éxito!")
        else:
            st.error("No se encontró solución. Revisa si el inicio o fin están bloqueados.")
            render_maze(MAZE)

with col2:
    if solve_btn and path:
        st.subheader("Resultados")
        st.metric(label="⏱️ Tiempo de Ejecución", value=f"{elapsed_ms:.4f} ms")
        st.metric(label="👣 Pasos Totales", value=f"{len(path)}")
        
        st.markdown("---")
        st.markdown("**Análisis:**")
        if "BFS" in algo_option:
            st.write("BFS garantiza el camino más corto explorando por niveles.")
        elif "DFS" in algo_option:
            st.write("DFS explora profundamente. El camino suele ser más largo y errático, pero usa menos memoria en mapas muy anchos.")
        elif "A*" in algo_option:
            st.write("A* es inteligente. Usa la distancia a la meta para priorizar caminos, encontrando la solución óptima (igual que BFS) pero más rápido.")
