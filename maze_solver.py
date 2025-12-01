import streamlit as st
import time
# IMPORTANTE: Aquí importamos desde tu otro archivo 'applaberinto'
from applaberinto import MAZE, START, END, solve_maze_bfs

st.set_page_config(page_title="Maze Solver", page_icon="🧩")

st.title("Visualizador de Algoritmo de Búsqueda")
st.markdown("Algoritmo implementado: **Breadth-First Search (BFS)**")

# Función para renderizar el laberinto con un poco de estilo CSS para alineación
def render_maze(maze, path=None):
    if path is None:
        path = []
    
    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            if (r_idx, c_idx) == START:
                display_row.append("🟢") # Inicio (Círculo verde)
            elif (r_idx, c_idx) == END:
                display_row.append("🏁") # Fin (Bandera)
            elif (r_idx, c_idx) in path:
                display_row.append("🟦") # Camino resuelto (Cuadrado azul)
            elif col == 1:
                display_row.append("⬛") # Muro (Cuadrado negro)
            else:
                display_row.append("⬜") # Camino libre (Cuadrado blanco)
        
        # Unimos la fila sin espacios extraños
        display_maze.append("".join(display_row))
    
    # Usamos CSS para ajustar el interlineado y que parezca una cuadrícula real
    st.markdown(
        f"""
        <div style="font-family: monospace; line-height: 1.0; font-size: 20px;">
            {'<br>'.join(display_maze)}
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- Sidebar para controles ---
st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox(
    "Selecciona el algoritmo", 
    ["BFS (Búsqueda en Amplitud)", "DFS (no implementado)", "A* (no implementado)"]
)
solve_button = st.sidebar.button("Resolver Laberinto")

# --- Lógica Principal ---

# 1. Mostrar estado inicial
if not solve_button:
    st.subheader("Laberinto Inicial")
    render_maze(MAZE)

# 2. Resolver al presionar el botón
if solve_button:
    if "BFS" in algorithm:
        st.subheader("Resolviendo...")
        
        # Inicio del cronómetro
        start_time = time.perf_counter()
        
        # Ejecución del algoritmo
        path = solve_maze_bfs(MAZE, START, END)
        
        # Fin del cronómetro
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000 # Convertir a milisegundos

        if path:
            st.success(f"¡Camino encontrado! Longitud de pasos: {len(path)}")
            # Mostrar tiempo con 4 decimales
            st.info(f"⏱️ Tiempo de ejecución: **{elapsed_time:.4f} ms**")
            
            st.subheader("Laberinto Resuelto")
            render_maze(MAZE, path)
        else:
            st.error("No se encontró un camino posible.")
            render_maze(MAZE)
    else:
        st.warning(f"El algoritmo {algorithm} aún no está implementado. Por favor usa BFS.")
