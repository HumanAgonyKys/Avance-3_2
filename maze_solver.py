import streamlit as st
import time
from applaberinto import MAZE, START, END, solve_maze_bfs, solve_maze_dfs, solve_maze_astar

st.set_page_config(page_title="Maze Solver Retro", layout="centered")

st.title("🏰 Solucionador de Laberinto")
st.markdown("Estilo clásico con visualización de bloques.")

# --- FUNCIÓN DE RENDERIZADO (TEXTO/EMOJIS) ---
def render_maze(maze, path=None):
    if path is None:
        path = []
    path_set = set(path) # Convertimos a set para búsqueda rápida
    
    rows = len(maze)
    cols = len(maze[0])
    
    html_maze = []
    
    # Construimos el laberinto fila por fila
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            # Prioridad de íconos
            if (r, c) == START:
                symbol = "🟢" # Inicio
            elif (r, c) == END:
                symbol = "🏁" # Fin
            elif (r, c) in path_set:
                symbol = "🟦" # Camino resuelto
            elif maze[r][c] == 1:
                symbol = "⬛" # Pared
            else:
                symbol = "⬜" # Pasillo vacío
            
            row_str += symbol
        html_maze.append(row_str)
    
    # CSS ajustado para compactar las líneas y que se vea mejor
    st.markdown(
        f"""
        <div style="
            font-family: monospace; 
            line-height: 12px; 
            font-size: 12px; 
            letter-spacing: 0px; 
            white-space: pre; 
            text-align: center;
            border: 4px solid #333;
            padding: 10px;
            background-color: #222;
            color: white;
            display: inline-block;
        ">
            {'<br>'.join(html_maze)}
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- BARRA LATERAL ---
st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox("Algoritmo", ["BFS (Amplitud)", "DFS (Profundidad)", "A* (A-Star)"])
solve_btn = st.sidebar.button("Resolver")

# --- LÓGICA PRINCIPAL ---
if not solve_btn:
    st.subheader("Laberinto Inicial")
    render_maze(MAZE)
else:
    st.subheader(f"Resultado: {algorithm}")
    
    path = None
    start_time = time.perf_counter()
    
    # Ejecutar algoritmo seleccionado
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
        st.success(f"¡Camino encontrado!")
        
        # Métricas
        c1, c2 = st.columns(2)
        c1.metric("Tiempo", f"{elapsed_time:.4f} ms")
        c2.metric("Pasos", len(path))
    else:
        st.error("No se encontró solución.")
        render_maze(MAZE)
