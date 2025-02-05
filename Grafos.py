import numpy as np
from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import scipy as sp

class Graph:
    def __init__(self, graph = None, directed=False, weighted=False):
        if graph is None:
            graph = {}
        self.graph = graph
        self.weighted = weighted
        self.directed = directed
        if weighted:
            self.directed = True
        self.index_map = {}
    
    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = {}
            self.graph = dict(sorted(self.graph.items()))
            return f"Vertex {v} Added"
        return "Vertex Already in Graph"
    
    def add_edge(self, u, v, weight=1):
        if weight is not None and weight<= 0:
            return "Weight needs to be greater than 0 (zero)."
        msg = ''
        if u not in self.graph:
            self.add_vertex(u)
            msg += f"\nVertex {u} Added"
        if v not in self.graph:
            self.add_vertex(v)
            msg += f"\nVertex {v} Added"
        if v not in self.graph[u].keys():
            self.graph[u][v] = weight
            if not self.directed:
                if u not in self.graph[v]:
                    self.graph[v][u] = weight
                    self.graph = dict(sorted(self.graph.items()))
                    return f"Edges {u}-{v} and {v}-{u} Added"+msg
            self.graph = dict(sorted(self.graph.items()))
            return f"Edge {u}-{v} Added"+msg
        return "Edge Already in Graph"
    
    def edit_weight(self, u, v, weight):
        if weight is not None and weight<= 0:
            return "Weight needs to be greater than 0 (zero)."
        if u in self.graph and v in self.graph:
            self.graph[u][v] = weight
            if not self.directed:
                self.graph[v][u] = weight
            return f"Weight of edge {u}-{v} altered to {weight}"
        else:
            return "Vertix or Edge not in Graph"
        
    def remove_vertex(self, v):
        if v not in self.graph.keys():
            return "Invalid Vertex"
        del self.graph[v]
        for neighbors in self.graph.values():
            if v in neighbors:
                del neighbors[v]
        self.update_index_map()
        return f"Vertex {v} Removed"
    
    def remove_edge(self, u, v):
        if u in self.graph and v in self.graph[u]:
            del self.graph[u][v]
            if not self.directed:
                del self.graph[v][u]
                return f"Edges {u}-{v} and {v}-{u} Removed"
            return f"Edge {u}-{v} Removed"
        return "Edge(s) not connected!"

    def show_size(self):
        vertices = sorted(self.graph.keys())
        size = len(vertices)
        return size
    
    def adjacency_matrix(self):
        self.update_index_map()  # Ensure the index_map is always up-to-date
        size = len(self.index_map)
        matrix = np.zeros((size, size), dtype=int)
        for v, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                i, j = self.index_map[v], self.index_map[neighbor]
                matrix[i][j] = weight
        return matrix
    
    def update_index_map(self):
        vertices = sorted(self.graph.keys())
        self.index_map = {vertices[i]: i for i in range(len(vertices))}

    def print_matrix(self):
        matrix = self.adjacency_matrix()
        size = len(matrix)
        for i in range(size):
            line = "|"
            for j in range(size):
                line += f' {matrix[i][j]} '
            line += "|"
            print(line)

    def bfs(self, start, search = None):
        vertices = sorted(self.graph.keys())
        if start not in vertices:
            return
        if search is not None and search not in vertices:
            return
        visited = set()
        queue = [start]
        result = []

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                if search is not None and vertex == search:
                    break

                for v in sorted(self.graph[vertex]):
                    if v not in visited:
                        queue.append(v)

        for vertex in vertices:
            if vertex not in visited:
                result.append(vertex)
        
        return result
    
    def dfs(self, start, search = None, cut = False):
        vertices = sorted(self.graph.keys())
        if start not in vertices:
            return
        if search is not None and search not in vertices:
            return
        visited = set()
        stack = [start]
        result = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                if search is not None and vertex == search:
                    break
                
                for v in reversed(sorted(self.graph[vertex])):
                    if v not in visited:
                        stack.append(v)
        if cut:
            for vertex in vertices:
                if vertex not in visited:
                    result.append(vertex)   
        
        return result

    def ftd(self, start):
        vertices = sorted(self.graph.keys())
        if start not in vertices:
            return "Invalid Vertex"
        visited = set()
        levels = {}
        queue = [start]
        levels[start] = 0

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                
                for v in self.graph[vertex]:
                    if v not in visited:
                        queue.append(v)
                        if v not in levels.keys():
                            levels[v] = levels[vertex] + 1

        for vertex in vertices:
            if vertex not in visited:
                levels[vertex] = -1

        return visited, {k: levels[k] for k in sorted(levels)}
    
    def fti(self, end):
        vertices = sorted(self.graph.keys())
        if end not in vertices:
            return "Invalid Vertex"
        
        # Inversão do grafo (chaves viram dados/dados viram chaves)
        igraph = {v: [] for v in self.graph} 
        for vertex in self.graph:
            for adjacent in self.graph[vertex]:
                igraph[adjacent].append(vertex)
        
        visited = set()
        levels = {}
        queue = [end]
        levels[end] = 0

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)

                for v in igraph[vertex]:
                    if v not in visited:
                        queue.append(v)
                        if v not in levels.keys():
                            levels[v] = levels[vertex] + 1
        
        for vertex in vertices:
            if vertex not in visited:
                levels[vertex] = -1
        
        return visited, {k: levels[k] for k in sorted(levels)}
    
    def connectivity(self, start):
        vertices = set(self.graph.keys())
        fw = self.ftd(start)[0]
        bw = self.fti(start)[0]
        return fw.intersection(bw), True if fw.intersection(bw) == vertices else False
        
    def find_all_subgraphs(self, start):
        vertices = set(self.graph.keys())
        visited = set()
        subgraphs = []
        
        subgraphs.append(self.connectivity(start)[0])
        visited.update(self.connectivity(start)[0])
        if self.connectivity(start)[1] == False:
            for vertex in vertices:
                if vertex not in visited:
                    subgraphs.append(self.connectivity(vertex)[0])
                    visited.update(self.connectivity(vertex)[0])
        return subgraphs
    
    def triangle_cycles(self):
        for node in self.graph:
            neighbors = list(self.graph[node])
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if neighbors[j] in self.graph[neighbors[i]]:
                        return True  # Found a triangle
        return False  # No triangle found

    def count_edges(self):
        edge_count = 0
        for node, neighbors in self.graph.items():
            edge_count += len(neighbors)
        return edge_count // (1 if self.directed else 2)
    
    def is_planar(self):
        V = len(self.graph)
        E = self.count_edges()
        if V >= 3:
            if E > 3 * V - 6:
                return False
            elif (self.triangle_cycles()) == False:
                if E > 2 * V - 4:
                    return False
            else:
                return True
        return True
    
    def count_faces(self):
        if self.graph == {}:
            return None
        V = len(self.graph)
        E = self.count_edges()
        if self.is_planar() and self.connectivity(list(self.graph.keys())[0])[1]:
            F = E+2-V
            return F
        else:
            return None
    
    def find_degrees(self):
        degrees = {}
        for vertix, neighbors in self.graph.items():
            degrees[vertix] = len(neighbors)
        return degrees
    
    def define_colors(self):
        degrees = self.find_degrees()
        colors = {}
        available = {}
        for vertix in self.graph:
            available[vertix] = set(range(len(self.graph))) 

        for vertix in sorted(degrees, key=degrees.get, reverse=True): 
            used_colors = {colors[neighbor] for neighbor in self.graph[vertix].keys() if neighbor in colors}
            for color in available[vertix]:
                if color not in used_colors:
                    colors[vertix] = color
                    break
        return colors
    
    def is_directed(self):
        for node in self.graph:
            for neighbor in self.graph[node]:
                if node not in self.graph[neighbor]:
                    return True
                if self.graph[node][neighbor] != self.graph[neighbor][node]:
                    return True
        return False
    
    def draw_graph(self, canvas_frame):
        if self.is_directed():
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        for node in self.graph:
            G.add_node(node)

        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                if self.is_directed():  # Assuming this is a method, not an attribute
                    # Check if the reverse edge exists (neighbor -> node)
                    if G.has_edge(neighbor, node):
                        # If the reverse edge exists, add the weight for the reverse edge
                        G[neighbor][node].update({'weight_vu': weight})
                        G.add_edge(node, neighbor, weight=weight, wight_vu=G[neighbor][node]['weight'])
                    else:
                        # Add the edge in the forward direction
                        G.add_edge(node, neighbor, weight=weight)
                else:
                    # For undirected graphs, just add the edge with the given weight
                    G.add_edge(node, neighbor, weight=weight)

        

        node_colors = self.define_colors()
        color_map = {
            0: 'green',
            1: 'blue',
            2: 'red',
            3: 'yellow',
            4: 'purple',
            5: 'orange',
            6: 'pink',
            7: 'brown',
            8: 'cyan',
            9: 'magenta',
            10: 'lime',
            11: 'olive',
            12: 'navy',
            13: 'teal',
            14: 'maroon',
            15: 'violet',
            16: 'turquoise',
            17: 'gold',
            18: 'salmon',
            19: 'beige'
        }
        colors_to_draw = [color_map[node_colors[node]] for node in G.nodes()]

        fig, ax = plt.subplots(figsize=(7.5, 5.75))
        try:
            pos = nx.planar_layout(G)
        except:
            pos = nx.spring_layout(G)
        
        if self.is_directed():
            nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', ax=ax)
        else:
            nx.draw(G, pos, with_labels=True, node_color=colors_to_draw, font_weight='bold', ax=ax)

        if self.weighted:
            # Create custom edge labels to display weights
            edge_labels = {}
            for u, v, data in G.edges(data=True):
                forward_weight = data.get('weight', 'N/A')
                
                # Check if the reverse edge exists and get its weight
                reverse_weight = G[v][u].get('weight', 'N/A') if G.has_edge(v, u) else None
                
                # Create a label based on the presence of the reverse weight
                if reverse_weight is not None:  # Reverse weight exists
                    edge_labels[(u, v)] = f"{u}{v}: {forward_weight} | {v}{u}: {reverse_weight}"
                else:  # No reverse weight
                    edge_labels[(u, v)] = f"{forward_weight}"  # Only show forward weight
                

            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        return fig
    
    def save_graph(self, file_path):
        if file_path:
            with open(file_path, 'w') as json_file:
                self.graph['weighted'] = self.weighted
                json.dump(self.graph, json_file, indent=4)
            return True, file_path
        else:
            return False, file_path

    def saveas_graph(self):
        root = tk.Tk()
        root.withdraw() 

        file_path = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as json_file:

                self.graph['weighted'] = self.weighted
                json.dump(self.graph, json_file, indent=4)
            root.destroy()
            return True, file_path
        else:
            root.destroy()
            return False, file_path

    def open_graph(self):
        root = tk.Tk()
        root.withdraw()

        file_path = tk.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as json_file:
                self.graph = json.load(json_file)
                self.weighted = self.graph['weighted']
                if self.weighted:
                    self.directed = True
                del self.graph['weighted']
            root.destroy()
            return True, file_path
        else:
            root.destroy()
            return False, file_path
        
    def clear_graph(self):
        if self.graph is not {}:
            self.graph = {}

    def graph_specs(self):
        specs = {
            'Planar': self.is_planar() if self.graph != {} else 'No Graph',
            'Chromatic Number': len(set(self.define_colors().values())) if not self.is_directed() else 'Counted only for undirected graphs',
            'Connectivity': self.connectivity(list(self.graph.keys())[0])[1] if self.graph != {} else False,
            'Directed': self.is_directed(),
            '#Nodes': len(self.graph),
            '#Edges': self.count_edges(),
            '#Faces': self.count_faces() if self.count_faces() else 'Counted only for simple planar connected graphs'
        }
        return specs
    


''' 
g = Graph(directed=False)
g.add_edge('C', 'D')
g.add_edge('A', 'B')
g.add_edge('D', 'F')
g.add_edge('E', 'F')
g.add_edge('E', 'A')
print(g.graph_specs())

print(g.adjacency_matrix())

print(g.find_degrees())
print(g.define_colors())

print(g.ftd('A'))
print(g.fti('A'))
print(g.dfs('A'))
print(g.dfs('F'))
print(g.connectivity('A')[1])
print(g.find_all_subgraphs('A'))
'''
