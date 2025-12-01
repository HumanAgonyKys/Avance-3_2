import streamlit as st
import time
from applaberinto import MAZE, START, END, solve_maze_bfs, solve_maze_dfs, solve_maze_astar

st.set_page_config(page_title="Maze Solver", layout="wide")

st.title("Visualizador de Laberintos")

# --- Diagnóstico Inicial ---
st.sidebar.subheader("Diagnóstico del Mapa")
rows = len(MAZE)
cols = len(MAZE[0]) if rows > 0 else 0
st.sidebar.write(f"Dimensiones: {rows} filas x {cols} columnas")
st.sidebar.write(f"Inicio {START}: {'✅ Libre' if MAZE[START[0]][START[1]]==0 else '❌ MURO'}")
st.sidebar.write(f"Meta {END}: {'✅ Libre' if MAZE[END[0]][END[1]]==0 else '❌ MURO'}")

def render_maze(maze, path=None):
    if path is None:
        path = []
    path_set = set(path)
    
    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            # Prioridad de renderizado
            if (r_idx, c_idx) == START:
                display_row.append("🚀") 
            elif (r_idx, c_idx) == END:
                display_row.append("🏁") 
            elif (r_idx, c_idx) in path_set:
                display_row.append("🟦") # Camino
            elif col == 1:
                display_row.append("⬛") # Muro
            else:
                display_row.append("⬜") # Pasillo
        display_maze.append("".join(display_row))
    
    st.markdown(
        f"""
        <div style="
            font-family: monospace; 
            line-height: 10px; 
            font-size: 10px; 
            white-space: pre; 
            overflow-x: auto;
            text-align: center;
        ">
            {'<br>'.join(display_maze)}
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- Panel de Control ---
algorithm = st.sidebar.selectbox("Algoritmo", ["BFS", "DFS", "A*"])
solve_btn = st.sidebar.button("Resolver")

col_main, col_stats = st.columns([3, 1])

with col_main:
    if not solve_btn:
        st.subheader("Laberinto Original")
        render_maze(MAZE)
    else:
        st.subheader(f"Resultado usando {algorithm}")
        start_time = time.perf_counter()
        
        path = None
        try:
            if algorithm == "BFS":
                path = solve_maze_bfs(MAZE, START, END)
            elif algorithm == "DFS":
                path = solve_maze_dfs(MAZE, START, END)
            elif algorithm == "A*":
                path = solve_maze_astar(MAZE, START, END)
        except Exception as e:
            st.error(f"Error ejecutando el algoritmo: {e}")
        
        end_time = time.perf_counter()
        
        if path:
            render_maze(MAZE, path)
            st.success("¡Laberinto Resuelto!")
        else:
            st.error("No se encontró solución o los puntos de inicio/fin están bloqueados.")
            render_maze(MAZE)

with col_stats:
    if solve_btn and path:
        elapsed = (end_time - start_time) * 1000
        st.metric("Tiempo (ms)", f"{elapsed:.4f}")
        st.metric("Pasos", len(path))
