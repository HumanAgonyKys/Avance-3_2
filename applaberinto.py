import collections
import heapq

# --- 1. DEFINICIÓN DEL LABERINTO ---
# Usamos raw string (r"") y strip() para evitar errores de espacios
maze_str = r"""
10111111111111111111111111111111
10100010001000000000100000000011
10101010101111101110111011111011
10001000101000001010000010001001
11111111101011111011111110101111
10000000101000001000001000100011
11101111101011101011101111101011
10001000001010001010001000001011
10111011111110111010111011111111
10100010001000100010001010000001
10101110101011101111101010111111
10101000100010001000101010001011
10101010111110101011101011101011
10001010100010101000000010001001
10111110101010101011111110111111
10000010101010101000100010000011
11111010101010101110101011111011
10000010001010101000101000001011
10111110111010101111101110101011
10001000100010100000000010101011
11101111101111101111111110101011
10101000001000101000100000101011
10101011111010101010101111111011
10101000100010101010001000000011
10101110101110111010111011111111
10001000101010001010100010000011
10111011101011101011101110111011
10001000001000101000001000100011
11101110111011101011111010111011
10100010000010001010000010001001
10111010111110111010111111101111
10100010100000101010100010001011
10101111101111101010101010111011
10100000101000001010101000101001
10111110101010111011101111101011
10000000001010000000000000000001
11111111111111111111111111111101
"""

# Limpiamos el string y creamos la matriz asegurando que no haya lineas vacias
MAZE = []
for line in maze_str.strip().split('\n'):
    clean_line = line.strip()
    if clean_line:
        MAZE.append([int(c) for c in clean_line])

# --- 2. CONFIGURACIÓN DE PUNTOS ---
rows = len(MAZE)
cols = len(MAZE[0])

# COORDENADAS FIJAS basadas en tu imagen y el texto
START = (0, 1)            # Fila 0, Columna 1 (La segunda casilla superior)
END = (rows - 1, cols - 2) # Última fila, penúltima columna

# --- 3. FUNCIONES AUXILIARES ---

def is_valid_point(maze, point):
    """Verifica si un punto es transitable (0) y está dentro de los límites."""
    r, c = point
    if 0 <= r < len(maze) and 0 <= c < len(maze[0]):
        return maze[r][c] == 0
    return False

def get_neighbors(maze, row, col):
    rows, cols = len(maze), len(maze[0])
    # Orden: Abajo, Derecha, Arriba, Izquierda
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbors = []
    
    for dr, dc in moves:
        n_row, n_col = row + dr, col + dc
        if 0 <= n_row < rows and 0 <= n_col < cols:
            if maze[n_row][n_col] == 0:
                neighbors.append((n_row, n_col))
    return neighbors

# --- 4. ALGORITMOS ---

def solve_maze_bfs(maze, start, end):
    if not is_valid_point(maze, start) or not is_valid_point(maze, end):
        return None 
        
    queue = collections.deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        (curr, path) = queue.popleft()
        if curr == end:
            return path

        for neighbor in get_neighbors(maze, curr[0], curr[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

def solve_maze_dfs(maze, start, end):
    if not is_valid_point(maze, start) or not is_valid_point(maze, end):
        return None

    # Usamos pila iterativa para evitar errores de recursión máxima en mapas grandes
    stack = [(start, [start])]
    visited = set()
    
    while stack:
        (curr, path) = stack.pop()
        
        if curr == end:
            return path
        
        if curr not in visited:
            visited.add(curr)
            # Agregamos vecinos
            for neighbor in get_neighbors(maze, curr[0], curr[1]):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None

def heuristic(a, b):
    # Distancia Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_astar(maze, start, end):
    if not is_valid_point(maze, start) or not is_valid_point(maze, end):
        return None

    queue = [] # Priority Queue
    # Tupla: (costo_f, nodo_actual, camino)
    heapq.heappush(queue, (0, start, [start]))
    visited = set()
    g_score = {start: 0}

    while queue:
        _, curr, path = heapq.heappop(queue)

        if curr == end:
            return path
        
        if curr in visited:
            continue
        visited.add(curr)

        for neighbor in get_neighbors(maze, curr[0], curr[1]):
            new_g = g_score[curr] + 1
            
            if new_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_g
                f_score = new_g + heuristic(neighbor, end)
                heapq.heappush(queue, (f_score, neighbor, path + [neighbor]))
    
    return None
