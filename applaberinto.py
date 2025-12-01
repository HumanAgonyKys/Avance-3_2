import collections

# Configuración del laberinto
# 0: camino libre, 1: muro
MAZE = [
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 1, 0, 0, 0]
]

START = (0, 0)
END = (9, 9)

def solve_maze_bfs(maze, start, end):
    """Resuelve el laberinto usando BFS y retorna el camino."""
    rows, cols = len(maze), len(maze[0])
    
    # Cola almacena: (coordenada_actual, camino_hasta_aqui)
    queue = collections.deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        (curr_row, curr_col), path = queue.popleft()

        if (curr_row, curr_col) == end:
            return path

        # Movimientos: Arriba, Abajo, Izquierda, Derecha
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row, next_col = curr_row + dr, curr_col + dc

            # Verificamos límites del mapa
            if 0 <= next_row < rows and 0 <= next_col < cols:
                # Verificamos que no sea muro (1) y no haya sido visitado
                if maze[next_row][next_col] == 0 and (next_row, next_col) not in visited:
                    visited.add((next_row, next_col))
                    new_path = path + [(next_row, next_col)] # Crea una nueva lista con el nuevo paso
                    queue.append(((next_row, next_col), new_path))
    
    return None # No se encontró camino
