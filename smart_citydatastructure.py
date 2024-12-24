import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

class CityGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_road(self, from_node, to_node, length, capacity, speed_limit, flow=0):
        self.graph.add_edge(from_node, to_node, length=length, capacity=capacity, speed_limit=speed_limit, flow=flow)
    
    def add_sensor(self, node, sensor_type, sensor_data):
        if node not in self.graph:
            self.graph.add_node(node)
        self.graph.nodes[node][sensor_type] = sensor_data

    def update_sensor_data(self, node, sensor_type, sensor_data):
        if node in self.graph and sensor_type in self.graph.nodes[node]:
            self.graph.nodes[node][sensor_type].update(sensor_data)
        else:
            self.add_sensor(node, sensor_type, sensor_data)
    
    def get_graph(self):
        return self.graph

def calculate_travel_time(u, v, edge_data):
    flow = edge_data.get('flow', 0)
    capacity = edge_data.get('capacity', 1)
    if flow < capacity:
        speed = edge_data['speed_limit']
    else:
        speed = edge_data['speed_limit'] * (capacity / flow)
    travel_time = edge_data['length'] / speed
    return travel_time

def dijkstra_optimized_path(graph, start_node, end_node):
    path = nx.shortest_path(graph, start_node, end_node, weight=calculate_travel_time)
    travel_times = [calculate_travel_time(u, v, graph[u][v]) for u, v in zip(path[:-1], path[1:])]
    total_travel_time = sum(travel_times)
    return path, total_travel_time
def predict_air_quality(sensor_data, periods=5):
    air_quality_series = pd.Series(sensor_data)
    
    model = SARIMAX(air_quality_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    try:
        model_fit = model.fit(disp=False)
        forecast = model_fit.forecast(steps=periods)
    except ValueError as e:
        print(f"Error fitting model: {e}")
        forecast = pd.Series([None]*periods)
    return forecast

def visualize_graph(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 8))
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
    
    edge_labels = {(u, v): f"{d['length']}km" for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red")
    
    plt.title("Traffic intersection graph")
    plt.show()

if __name__ == "__main__":
    city_graph = CityGraph()

    roads = [
        ('Intersection_1', 'Intersection_2', 2.5, 2000, 60, 1500),
        ('Intersection_2', 'Intersection_3', 3.0, 1800, 50, 1600),
        ('Intersection_3', 'Intersection_4', 1.2, 1500, 40, 1400),
        ('Intersection_4', 'Intersection_5', 4.0, 2200, 70, 2000),
        ('Intersection_5', 'Intersection_1', 3.5, 2000, 60, 1800),
        ('Intersection_2', 'Intersection_5', 2.8, 1900, 55, 1700),
        ('Intersection_1', 'Intersection_4', 3.6, 2100, 65, 1900),
        ('Intersection_3', 'Intersection_5', 1.5, 1600, 45, 1500)
    ]

    for road in roads:
        city_graph.add_road(*road)

    
    sensors = [
        ('Intersection_1', 'traffic', {'flow': 150, 'speed': 50}),
        ('Intersection_2', 'air_quality', {'AQI': 45}),
        ('Intersection_3', 'traffic', {'flow': 300, 'speed': 40}),
        ('Intersection_4', 'air_quality', {'AQI': 60}),
        ('Intersection_5', 'traffic', {'flow': 250, 'speed': 55}),
        ('Intersection_2', 'traffic', {'flow': 200, 'speed': 48}),
        ('Intersection_4', 'traffic', {'flow': 350, 'speed': 38}),
        ('Intersection_1', 'air_quality', {'AQI': 50})
    ]

    for sensor in sensors:
        city_graph.add_sensor(*sensor)

    G = city_graph.get_graph()
    print("Graph Nodes:", G.nodes(data=True))
    print("Graph Edges:", G.edges(data=True))

    
    visualize_graph(G)

    
    shortest_path, total_travel_time = dijkstra_optimized_path(G, 'Intersection_1', 'Intersection_4')
    print("Optimized path from Intersection_1 to Intersection_4:", shortest_path)
    print("Total travel time:", total_travel_time)

   
    air_quality_data = [45, 48, 50, 47, 49, 52, 54, 55, 58, 60, 63, 65, 67, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90]
    predicted_aqi = predict_air_quality(air_quality_data)
    print("Predicted AQI for next periods:", predicted_aqi)
