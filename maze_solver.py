import streamlit as st
import time
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# Importamos la lógica
from applaberinto import MAZE, START, END, solve_maze_bfs, solve_maze_dfs, solve_maze_astar

st.set_page_config(page_title="Maze Solver Pro", layout="centered")

st.title("🧩 Solucionador de Laberintos")
st.markdown("Algoritmos: **BFS**, **DFS** y **A***")

# --- FUNCIÓN DE RENDERIZADO GRÁFICO ---
def render_maze_plot(maze, path=None):
    """
    Dibuja el laberinto usando Matplotlib para garantizar cuadros perfectos.
    """
    # 1. Convertimos la lista de listas en un array de numpy para manipularlo fácil
    maze_np = np.array(maze)
    
    # 2. Creamos una matriz de "colores" (mapa de visualización)
    # 0 = Camino (Blanco)
    # 1 = Muro (Negro)
    # 2 = Solución (Azul)
    # 3 = Inicio (Verde)
    # 4 = Fin (Rojo)
    
    # Copiamos para no modificar el original
    display_grid = maze_np.copy()
    
    # Si hay un camino, lo marcamos con el número 2
    if path:
        for (r, c) in path:
            if (r, c) != START and (r, c) != END:
                display_grid[r][c] = 2
    
    # Marcamos Inicio (3) y Fin (4)
    display_grid[START] = 3
    display_grid[END] = 4

    # 3. Definimos los colores personalizados
    # El orden corresponde a los números: 0, 1, 2, 3, 4
    # 0: Blanco, 1: Negro, 2: Azul Claro, 3: Verde, 4: Rojo
    cmap = ListedColormap(['#ffffff', '#000000', '#3399ff', '#00cc00', '#cc0000'])
    
    # 4. Crear la figura
    fig, ax = plt.subplots(figsize=(8, 8)) # Tamaño cuadrado
    ax.imshow(display_grid, cmap=cmap, interpolation='nearest')
    
    # Quitar los ejes (números de los lados) para que se vea limpio
    ax.axis('off')
    
    # Mostrar en Streamlit
    st.pyplot(fig)

# --- INTERFAZ ---
st.sidebar.header("Configuración")
algo_option = st.sidebar.selectbox(
    "Selecciona el Algoritmo:",
    ["BFS (Amplitud)", "DFS (Profundidad)", "A* (A-Star)"]
)

solve_btn = st.sidebar.button("🚀 Resolver", type="primary")

# --- LÓGICA DE EJECUCIÓN ---

if not solve_btn:
    st.subheader("Estado Inicial")
    render_maze_plot(MAZE)
else:
    st.subheader(f"Resultado: {algo_option}")
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
        st.error(f"Error: {e}")

    end_time = time.perf_counter()
    elapsed_ms = (end_time - start_time) * 1000

    if path:
        # Mostramos métricas
        col1, col2 = st.columns(2)
        col1.metric("Tiempo", f"{elapsed_ms:.4f} ms")
        col2.metric("Pasos", len(path))
        
        # Mostramos el laberinto resuelto
        render_maze_plot(MAZE, path)
        
        st.success("¡Meta alcanzada!")
    else:
        st.error("No se encontró camino.")
        render_maze_plot(MAZE)
