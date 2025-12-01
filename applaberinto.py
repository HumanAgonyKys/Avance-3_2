import collections
import heapq

# --- DEFINICIÓN DEL NUEVO LABERINTO ---
# Convertimos el string en una matriz de enteros
maze_str = """
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

# Procesamos el string para crear la lista de listas
MAZE = [[int(c) for c in line.strip()] for line in maze_str.strip().split('\n')]

# Detectamos inicio (fila 0, donde sea 0) y fin (última fila, donde sea 0)
START = (0, 1) # Basado en tu mapa visual
# Calculamos dinámicamente el final basado en el tamaño del mapa
rows = len(MAZE)
cols = len(MAZE[0])
END = (rows - 1, cols - 2) # Basado en tu mapa visual


def get_neighbors(maze, row, col):
    """Función auxiliar para obtener vecinos válidos."""
    rows, cols = len(maze), len(maze[0])
    # Orden de exploración: Abajo, Derecha, Arriba, Izquierda (Para DFS suele verse mejor)
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbors = []
    
    for dr, dc in moves:
        n_row, n_col = row + dr, col + dc
        if 0 <= n_row < rows and 0 <= n_col < cols:
            if maze[n_row][n_col] == 0:
                neighbors.append((n_row, n_col))
    return neighbors


def solve_maze_bfs(maze, start, end):
    """Algoritmo BFS: Garantiza el camino más corto en laberintos sin peso."""
    queue = collections.deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        (curr, path) = queue.popleft() # FIFO (First In, First Out)
        
        if curr == end:
            return path

        for neighbor in get_neighbors(maze, curr[0], curr[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None


def solve_maze_dfs(maze, start, end):
    """Algoritmo DFS: Explora caminos profundos. No garantiza el más corto."""
    stack = [(start, [start])] # Pila en lugar de Cola
    visited = set()
    # No marcamos visited al inicio en DFS iterativo para permitir backtracking natural
    # pero para laberintos simples, marcamos al procesar.
    
    while stack:
        (curr, path) = stack.pop() # LIFO (Last In, First Out)
        
        if curr in visited:
            continue
        visited.add(curr)

        if curr == end:
            return path

        # Agregamos vecinos a la pila
        for neighbor in get_neighbors(maze, curr[0], curr[1]):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return None


def heuristic(a, b):
    """Distancia Manhattan para A*"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve_maze_astar(maze, start, end):
    """Algoritmo A*: Usa heurística para encontrar el camino más corto rápidamente."""
    # Cola de prioridad almacena: (costo_f, nodo_actual, camino)
    # costo_f = costo_pasos_g + heuristica_h
    queue = []
    heapq.heappush(queue, (0, start, [start]))
    
    visited = set()
    
    # Costo g: costo para llegar al nodo desde el inicio
    g_score = {start: 0}

    while queue:
        # Obtiene el nodo con menor costo estimado
        _, curr, path = heapq.heappop(queue)

        if curr == end:
            return path
        
        if curr in visited:
            continue
        visited.add(curr)

        current_g = g_score[curr]

        for neighbor in get_neighbors(maze, curr[0], curr[1]):
            new_g = current_g + 1 # El peso de cada paso es 1
            
            # Si encontramos un camino mejor a este vecino o no lo hemos visitado
            if neighbor not in visited:
                 # Si no tiene g_score o encontramos uno mejor (aquí siempre es +1 así que simple)
                if new_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = new_g
                    f_score = new_g + heuristic(neighbor, end)
                    heapq.heappush(queue, (f_score, neighbor, path + [neighbor]))
    
    return None
