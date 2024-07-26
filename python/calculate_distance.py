import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations


class Graph:
    def __init__(self, place_file, road_file):
        # 传入地点信息格式示例：[0,'沙漠',1,1.0,3.5] [结点编号，名称，1表示该点有意义是一个地点，0表示该点无意义（为道路交叉点），横坐标，纵坐标]
        self.place_data = np.loadtxt(place_file, delimiter=',',
                                     dtype={'names': ('id', 'name', 'is_significant', 'x', 'y'),
                                            'formats': ('i4', 'U10', 'i4', 'f4', 'f4')})
        # 传入道路信息格式示例：[0,0,1,10.0] [道路编号，端点1，端点2，距离]
        self.road_data = np.loadtxt(road_file, delimiter=',', dtype={'names': ('road_id', 'start', 'end', 'distance'),
                                                                     'formats': ('i4', 'i4', 'i4', 'f4')})

        self.graph = self.build_graph()

    def build_graph(self):
        G = nx.Graph()
        for place in self.place_data:
            G.add_node(place['id'], pos=(place['x'], place['y']), is_significant=place['is_significant'])
        for road in self.road_data:
            G.add_edge(road['start'], road['end'], weight=road['distance'])
        return G

    def draw_graph(self):
        pos = {node: (data['pos'][0], data['pos'][1]) for node, data in self.graph.nodes(data=True)}
        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color='lightblue')
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()

    def find_shortest_path(self, start, places):
        # Extract subgraph with only the significant places and the start point
        subgraph = self.graph.subgraph([start] + places)

        # Find all permutations of places
        perms = permutations(places)
        min_path = None
        min_distance = float('inf')

        # Check all permutations to find the shortest path
        for perm in perms:
            path = [start] + list(perm) + [start]
            distance = sum(nx.dijkstra_path_length(subgraph, path[i], path[i + 1]) for i in range(len(path) - 1))
            if distance < min_distance:
                min_distance = distance
                min_path = path

        return min_path, min_distance


# Example usage:
# Initialize graph with place and road data
graph = Graph('places.csv', 'roads.csv')

# Draw the graph
graph.draw_graph()

# Define start point and significant places to visit
start_point = 0
significant_places = [place['id'] for place in graph.place_data if place['is_significant'] == 1]

# Find the shortest path
shortest_path, shortest_distance = graph.find_shortest_path(start_point, significant_places)

print(f"Shortest path: {shortest_path}")
print(f"Shortest distance: {shortest_distance}")

