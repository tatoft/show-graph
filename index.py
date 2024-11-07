import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Cargar el dataset
data = pd.read_csv('amazon_delivery.csv')

# Seleccionar 1500 registros aleatorios como se requiere en el proyecto
data_sample = data.sample(n=1500, random_state=42)

# Crear el grafo
G = nx.Graph()

# Añadir nodos y aristas al grafo basados en el dataset
for index, row in data_sample.iterrows():
    store_location = (row['Store_Latitude'], row['Store_Longitude'])
    drop_location = (row['Drop_Latitude'], row['Drop_Longitude'])
    
    # Añadir nodos con atributos relevantes
    G.add_node(store_location, 
               label='Store', 
               node_type='Store',
               traffic=row['Traffic'])
    
    G.add_node(drop_location, 
               label='Drop', 
               node_type='Drop',
               delivery_time=row['Delivery_Time'],
               vehicle=row['Vehicle'])
    
    # Calcular la distancia como peso de la arista
    distance = np.sqrt(
        (row['Drop_Latitude'] - row['Store_Latitude'])**2 + 
        (row['Drop_Longitude'] - row['Store_Longitude'])**2
    )
    
    # Añadir arista con atributos
    G.add_edge(store_location, drop_location, 
               weight=distance,
               traffic=row['Traffic'],
               delivery_time=row['Delivery_Time'],
               vehicle=row['Vehicle'])

# Configurar la figura
plt.figure(figsize=(18, 18))

# Usar un layout que distribuya mejor los nodos
pos = nx.spring_layout(G, k=0.3, iterations=40)

# Colores y tamaños de nodos basados en tipo y tráfico
node_colors = []
node_sizes = []
for node in G.nodes():
    if G.nodes[node]['node_type'] == 'Store':
        node_colors.append('red')  # Tiendas en rojo
        node_sizes.append(150)  # Tamaño más grande para tiendas
    else:
        # Colores de puntos de entrega según tráfico
        traffic = G.nodes[node].get('traffic', 'Low')
        if traffic == 'High':
            node_colors.append('darkred')
        elif traffic == 'Medium':
            node_colors.append('orange')
        else:
            node_colors.append('green')
        node_sizes.append(80)  # Tamaño más pequeño para puntos de entrega

# Colores y grosores de aristas basados en tiempo de entrega y tráfico
edge_colors = []
edge_widths = []
for (u, v) in G.edges():
    delivery_time = G[u][v]['delivery_time']
    # Normalizar el tiempo de entrega para el color
    normalized_time = min(delivery_time / 200.0, 1.0)  # Máximo tiempo considerado: 200 minutos
    edge_colors.append(plt.cm.YlOrRd(normalized_time))  # Colores de la arista según el tiempo de entrega
    # Ancho de línea basado en tráfico
    if G[u][v]['traffic'] == 'High':
        edge_widths.append(1.2)  # Mayor ancho para alto tráfico
    elif G[u][v]['traffic'] == 'Medium':
        edge_widths.append(0.8)
    else:
        edge_widths.append(0.4)

# Dibujar el grafo
nx.draw(G, pos,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color=edge_colors,
        width=edge_widths,
        with_labels=False,
        alpha=0.8)

# Añadir título y leyenda manual
plt.title("Red de Entregas de Amazon - Visualización de Tiendas y Puntos de Entrega", 
          fontsize=18, pad=20)

legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', label='Tienda', markersize=12),
                   plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', label='Entrega - Bajo tráfico', markersize=12),
                   plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', label='Entrega - Tráfico medio', markersize=12),
                   plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkred', label='Entrega - Alto tráfico', markersize=12)]

plt.legend(handles=legend_elements, loc='upper right', fontsize=12)

# Ajustar los márgenes
plt.tight_layout()

# Mostrar el gráfico
plt.show()

# Imprimir estadísticas de la red
print("\nEstadísticas de la Red de Entregas:")
print(f"Número total de nodos: {G.number_of_nodes()}")
print(f"Número total de rutas: {G.number_of_edges()}")
print("\nDistribución de tráfico:")
traffic_counts = data_sample['Traffic'].value_counts()
print(traffic_counts)
