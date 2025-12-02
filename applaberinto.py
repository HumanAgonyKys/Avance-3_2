import collections
import heapq

# --- DEFINICIÓN DEL LABERINTO (TEXTO EXACTO) ---
maze_raw = """
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

MAZE = []
for line in maze_raw.strip().split('\n'):
    clean_line = line.strip()
    if clean_line:
        MAZE.append([int(ch) for ch in clean_line])

rows = len(MAZE)
cols = len(MAZE[0])
START = (0, 1)
END = (rows - 1, cols - 2)

def get_neighbors(maze, row, col):
    rows_len, cols_len = len(maze), len(maze[0])
    deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbors = []
    for dr, dc in deltas:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows_len and 0 <= nc < cols_len:
            if maze[nr][nc] == 0:
                neighbors.append((nr, nc))
    return neighbors

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_bfs(maze, start, end):
    queue = collections.deque([(start, [start])])
    visited = set([start])
    while queue:
        (current, path) = queue.popleft()
        if current == end: return path
        for neighbor in get_neighbors(maze, current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

def solve_maze_dfs(maze, start, end):
    stack = [(start, [start])]
    visited = set()
    while stack:
        (current, path) = stack.pop()
        if current == end: return path
        if current in visited: continue
        visited.add(current)
        for neighbor in get_neighbors(maze, current[0], current[1]):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return None

def solve_maze_astar(maze, start, end):
    pq = []
    heapq.heappush(pq, (0, start, [start]))
    visited = set()
    g_score = {start: 0}
    while pq:
        _, current, path = heapq.heappop(pq)
        if current == end: return path
        if current in visited: continue
        visited.add(current)
        current_g = g_score[current]
        for neighbor in get_neighbors(maze, current[0], current[1]):
            new_g = current_g + 1
            if new_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_g
                f_score = new_g + heuristic(neighbor, end)
                heapq.heappush(pq, (f_score, neighbor, path + [neighbor]))
    return None
