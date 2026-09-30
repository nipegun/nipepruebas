import networkx as nx
import matplotlib.pyplot as plt

# Datos estructurados en formato JSON
data = [
    {"Sector": "Sector Público", "CSIRT": "CCN-CERT", "Autoridad": "Ministerio de Asuntos Económicos y Transformación Digital"},
    {"Sector": "Sector Privado", "CSIRT": "INCIBE-CERT", "Autoridad": "AEPD, CNMC, Ministerio del Interior, CCN (en casos específicos)"},
    {"Sector": "Infraestructuras Críticas", "CSIRT": "CCN-CERT, INCIBE-CERT", "Autoridad": "CNPIC"},
    {"Sector": "Internacional o Cooperación Europea", "CSIRT": "CSIRT Network", "Autoridad": "ENISA"}
]

# Crear un grafo dirigido
G = nx.DiGraph()

# Añadir nodos y relaciones
for item in data:
    G.add_edge(item["Sector"], item["CSIRT"])
    G.add_edge(item["CSIRT"], item["Autoridad"])

# Generar posiciones para los nodos
pos = nx.spring_layout(G)

# Dibujar el grafo
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
plt.title("Relación entre CSIRT y Autoridades por Sector", fontsize=14)
plt.show()
