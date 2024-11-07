pip install pandas
pip install sqlalchemy
pip install networkx



import pandas as pd
import numpy as np
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

# Conectar a la base de datos SQLite
conn = sqlite3.connect('amazon_delivery.db')

# Cargar los datos en un DataFrame
amazon_delivery_data = pd.read_sql_query("SELECT * FROM delivery", conn)
conn.close()

# Limpiar el DataFrame (eliminar la columna 'Weather')
amazon_delivery_data_cleaned = amazon_delivery_data.drop(columns=['Weather'])

# Definir la función de Haversine (para calcular distancias, aunque no la usaremos ahora)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c  # Devuelve la distancia en km

# Crear un grafo vacío
graph = nx.Graph()

# Función para agregar nodos y aristas al grafo
def add_nodes_and_edges(data):
    for index, row in data.iterrows():
        store_node = (row['Store_Latitude'], row['Store_Longitude'])
        drop_node = (row['Drop_Latitude'], row['Drop_Longitude'])
        
        # Agregar nodos al grafo
        graph.add_node(store_node)
        graph.add_node(drop_node)

        # Calcular la distancia y agregar una arista
        distance = haversine(row['Store_Latitude'], row['Store_Longitude'],
                             row['Drop_Latitude'], row['Drop_Longitude'])
        graph.add_edge(store_node, drop_node, weight=distance)

# Llamar a la función para agregar nodos y aristas
add_nodes_and_edges(amazon_delivery_data_cleaned)

# Visualizar el grafo
plt.figure(figsize=(10, 10))
pos = {node: (node[1], node[0]) for node in graph.nodes()}  # Cambiar el orden para matplotlib
nx.draw(graph, pos, with_labels=False, node_size=50, font_size=8, alpha=0.6)
plt.title("Grafo de Rutas de Entrega")
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.show()
