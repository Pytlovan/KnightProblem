import copy
import time
from Grafos import Graph
from enum import Enum
import numpy as np

# class Board:
#     # Initializes the board with a size
#     def __init__(self, size):
#         # Initializes the board with a size
#         self.size = size
#         # Initializes the connections with a Graph object
#         self.connections = Graph(weighted=False, directed=False)

#     # Function for valid jumps
#     def valid_jumps(self, x, y):
#         connections = {}
#         movements = {
#             1: (x-2, y-1),
#             2: (x-2, y+1),
#             3: (x-1, y-2),
#             4: (x-1, y+2),
#             5: (x+1, y-2),
#             6: (x+1, y+2),
#             7: (x+2, y-1),
#             8: (x+2, y+1)
#         }
#         for key, jump in movements.items():
#             i = jump[0]
#             j = jump[1]
#             if i >= 0 and i < self.size and j >=0 and j < self.size:
#                 connections[f"{i}{j}"] = 1
#         return connections

#     # create_board_connections: 8n => O(n) where n = vertix count (size²) // ex: 64*8
#     def create_board_connections(self):
#         connections = {}
#         for x in range(self.size):
#             for y in range(self.size):
#                 connections[f"{x}{y}"] = self.valid_jumps(x, y)
#         self.connections.graph = connections 

# class KnightProblem:
#     def __init__(self, size=8):
#         self.board = Board(size)
#         self.base_board = Board(size)
#         self.size = size
#         self.steps = 1
#         self.board.create_board_connections()
#         self.base_board.connections = copy.deepcopy(self.board.connections)  # Cópia profunda do grafo
#         self.matrix = [["" for _ in range(self.size)] for _ in range(self.size)]
#         self.convert = False
#         self.closed = False
        
#     # find_degrees: O(n) where n = vertix count (size²)
#     def create_matrix(self):
#         matrix = [["" for _ in range(self.size)] for _ in range(self.size)]
#         degrees = self.board.connections.find_degrees(self.board.connections)
#         for x in range(self.size):
#             for y in range(self.size):
#                 matrix[x][y] = degrees[f"{x}{y}"]
#         return matrix
    
#     def generate_heatmap(self):
#         N = self.size
#         center = (N - 1) / 2
#         heatmap = np.zeros((N, N))
        
#         for i in range(N):
#             for j in range(N):
#                 distance = ((i - center)**2 + (j - center)**2)/(center**2)
#                 value = 2/distance
#                 heatmap[i, j] = value
#         return heatmap
    
#     def generate_object_heatmap(self):
#         heatmap_object = {}
#         heatmap = self.generate_heatmap()
#         for i in range(self.size):
#             for j in range(self.size):
#                 heatmap_object[f"{i}{j}"] = heatmap[i][j]
#         return heatmap_object
    
#     def create_map(self, start):
#         matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
#         order = self.intelligent_path(start)
#         for key,value in order.items():
#             x, y = int(key[0]), int(key[1])
#             matrix[x][y] = value
#         return matrix
    
#     def save_board(self):
#         self.board.connections.weighted = False
#         self.board.connections.saveas_graph(self.board.connections)

#     def find_lowest_value(self, neighbours, next_lowest=0):
#         heatmap = self.generate_object_heatmap()
#         neighbours_size = {}

#         for neighbour in neighbours:
#             neighbours_size[neighbour] = heatmap[neighbour]

#         valid_neighbours = [k for k in neighbours_size if neighbours_size[k] > 0]
        
#         if not valid_neighbours:
#             return None
        
#           # Encontra o primeiro menor valor
#           # Remove apenas o primeiro menor valor encontrado
        
#         if next_lowest == 0:
#             min_key = min(valid_neighbours, key=neighbours_size.get)
#             return min_key if neighbours_size else None
#         else:
#             if next_lowest >= len(neighbours):
#                 return None
#             for _ in range(next_lowest):
#                 print(neighbours_size)
#                 min_key = min(valid_neighbours, key=neighbours_size.get)
#                 del neighbours_size[min_key]
#             return min(neighbours_size, key=neighbours_size.get) if neighbours_size else None

                

#     def find_lowest_move_degree(self, neighbours, board_state):
#         degrees = self.board.connections.find_degrees(board_state)
#         neighbours_size = {}

#         for neighbour in neighbours:
#             neighbours_size[neighbour] = degrees[neighbour]
        
#         valid_neighbours = [k for k in neighbours_size if neighbours_size[k] > 0]
#         return min(valid_neighbours, key=neighbours_size.get) if valid_neighbours else None

#     def intelligent_path(self, current_pos, order=None, current_board_state=None, find_next_lowest=0, count=1):
#         if order is None:
#             order = {}

#         base_board = self.base_board.connections.graph
#         current_board_state = self.board.connections  # Cópia para evitar alterações inesperadas
#         current_board_state.directed = False

#         order[current_pos] = count
#         neighbours = list(current_board_state.graph[current_pos].keys())


#         for square, jumps in current_board_state.graph.items():
#             if current_pos in jumps:
#                 current_board_state.remove_edge(square, current_pos)

#         lowest_square_degree = self.find_lowest_value(neighbours, find_next_lowest)

#         if lowest_square_degree:
#             self.steps += 1
#             return self.intelligent_path(lowest_square_degree, order, current_board_state, 0, count + 1)
#         else:
#             if len(order) == self.size * self.size:
#                 return order  # Solução encontrada!

#             # Backtracking
#             print("Não convergiu, fazendo backtracking...")
#             neighbours = list(base_board[current_pos].keys())

#             for neighbour in neighbours:
#                 current_board_state.add_edge(neighbour, current_pos)  # Revertendo remoção

#             del order[current_pos]  # Removendo última posição visitada

#             if not order:
#                 return None  # Nenhum caminho válido encontrado

#             return self.intelligent_path(list(order.keys())[-1], order, current_board_state, find_next_lowest + 1, count - 1)
    
#     def print_board(self, start):
#         self.matrix = self.create_map(start)
#         for linha in self.matrix:
#             print(linha)
import numpy as np

class KnightTour:
    def __init__(self, size=8):
        self.size = size
        self.board = [[-1 for _ in range(size)] for _ in range(size)]  # Inicializa o tabuleiro com -1
        self.moves_x = [-2, -1, 1, 2, 2, 1, -1, -2]  # Movimentos possíveis em X
        self.moves_y = [-1, -2, -2, -1, 1, 2, 2, 1]  # Movimentos possíveis em Y
        self.steps = 1
        
    def is_valid_move(self, x, y):
        """Verifica se um movimento é válido (dentro dos limites e não visitado)."""
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == -1

    def solve(self, start_x, start_y):
        """Inicia a solução do problema do cavalo."""
        self.board[start_x][start_y] = 1  # Define a posição inicial como 1

        if not self.solve_knight_tour(start_x, start_y, 2):
            print("Solução não encontrada.")
            return False
        else:
            self.print_board()
            return True
        
    def print_board(self):
        """Imprime o tabuleiro com o caminho do cavalo."""
        for row in self.board:
            print(" ".join(f"{num:3}" for num in row))
        print(f"Passos: {self.steps}")


class HeatMap(KnightTour):
    def __init__(self, size=8):
        super().__init__(size)
        self.heatmap = self.generate_heatmap()  # Gera a heatmap na inicialização

    def generate_heatmap(self):
        """Cria uma matriz de calor onde valores maiores indicam posições mais prioritárias."""
        N = self.size
        center = (N - 1) / 2
        heatmap = np.zeros((N, N))
        
        for i in range(N):
            for j in range(N):
                distance = ((i - center)**2 + (j - center)**2) / (center**2)
                value = 2 / (distance + 1e-5)  # Pequeno ajuste para evitar divisão por zero
                heatmap[i, j] = value
        return heatmap

    def solve_knight_tour(self, x, y, move_count):
        """Tenta resolver o problema do cavalo usando backtracking, priorizando posições mais quentes da heatmap."""
        if move_count == self.size * self.size + 1:
            return True

        # Gera os movimentos possíveis e ordena pelo maior valor da heatmap
        moves = []
        for i in range(8):
            next_x, next_y = x + self.moves_x[i], y + self.moves_y[i]
            if self.is_valid_move(next_x, next_y):
                priority = self.heatmap[next_x, next_y]
                moves.append((priority, next_x, next_y))

        # Ordena por maior valor na heatmap (do maior para o menor)
        moves.sort(reverse=False)

        for _, next_x, next_y in moves:
            self.board[next_x][next_y] = move_count  # Marca como visitado
            self.steps += 1
            
            if self.solve_knight_tour(next_x, next_y, move_count + 1):
                return True  # Se encontrou solução, retorna True
            
            self.board[next_x][next_y] = -1  # Backtracking

        return False  # Nenhum movimento válido encontrado

class BruteForce(KnightTour):
    def __init__(self, size=8):
        super().__init__(size)

    def solve_knight_tour(self, x, y, move_count):
        """Tenta resolver o problema do cavalo usando backtracking."""
        # Se todas as casas foram visitadas, terminamos
        if move_count == self.size * self.size + 1:
            return True

        # Tenta todos os 8 movimentos possíveis do cavalo
        for i in range(self.size):
            next_x = x + self.moves_x[i]
            next_y = y + self.moves_y[i]
            if self.is_valid_move(next_x, next_y):
                self.board[next_x][next_y] = move_count  # Marca como visitado
                self.steps += 1
                
                if self.steps > 1e8: # 100 milhões de steps 
                    return False
                
                if self.solve_knight_tour(next_x, next_y, move_count + 1):
                    return True  # Se encontrou solução, retorna True
                
                self.board[next_x][next_y] = -1

        return False  # Se nenhum movimento funcionou, retorna False

#------------------------------------------------------------
#Main

def create_column_enum(n):
    columns = {chr(65 + i): i for i in range(n)} 
    return Enum('Column', columns)

N = 8

Column = create_column_enum(N)

Start_Square = "D4"

x = N - int(Start_Square[1])
y = Column[Start_Square[0]].value

# Creates a KnightProblem object with the size of the board

bruteForce_knight = BruteForce(size = N)
smart_knight = HeatMap(size = N)

start_time = time.time()

smart_knight.solve(x, y)

end_time = time.time()

# Prints the number of steps
print("\nResult of Knight Problem\nIntelligent Path \n")
print(f"Time: {end_time - start_time:.6f}s")
print(f"Number of steps: {smart_knight.steps}")
print("\n")
# print(execution_time)

start_time2 = time.time()

bruteForce_knight.solve(x, y)

end_time2 = time.time()

print("\nResult of Knight Problem\nBacktracking Path\n")
print(f"Time: {end_time2 - start_time2:.6f}s")
print(f"Number of steps: {bruteForce_knight.steps}")
print("\n")