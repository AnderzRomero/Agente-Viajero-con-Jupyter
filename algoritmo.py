import csv
import networkx as nx
import matplotlib.pyplot as plt
import folium
import haversine


ciudades = []

with open('Agente Viajero\ciudades.csv', newline='') as csvfile:
      lectura = csv.reader(csvfile, delimiter=',')  
      next(lectura)
      for row in lectura:
        ciudad = row[0]
        latitud = float(row[1])
        longitud = float(row[2])
        ciudades.append((ciudad, latitud, longitud))
      print("Orden de la base de datos CSV")
      print(ciudades)

# Crear grafo de todas las ciudades
G = nx.complete_graph(len(ciudades))


# Calcular las distancias entre todas las ciudades
for i in range(len(ciudades)):
      for j in range(i+1, len(ciudades)):
          ciudad1 = ciudades[i]
          ciudad2 = ciudades[j]
          dist = haversine.haversine((ciudad1[1], ciudad1[2]), (ciudad2[1], ciudad2[2]))
          G.add_weighted_edges_from([(i, j, dist)])          
          
# Calcular la ruta óptima utilizando el algoritmo TSP
route = nx.algorithms.approximation.traveling_salesman_problem(G)
print("Rutas mas optimas")
print(route)

# Ordenar las ciudades según la ruta óptima y por nombre de cada ciudad
ordered_ciudades = [ciudades[i] for i in route]
print("Ruta mas optima por nombres de las ciudades")
print(ordered_ciudades)

# Crear mapa en la primera ciudad de la ruta óptima
mapa = folium.Map(location=[ordered_ciudades[0][1], ordered_ciudades[0][2]], zoom_start=5)


# Añadir marcadores para cada ciudad en la ruta
for ciudad in ordered_ciudades:
    folium.Marker(location=[ciudad[1], ciudad[2]],popup=[ciudad[1], ciudad[2]]).add_to(mapa)


# Añadir una línea que conecte todas las ciudades en la ruta
locations = [[ciudad[1], ciudad[2]] for ciudad in ordered_ciudades]
folium.PolyLine(locations=locations, weight=2.5, color='black').add_to(mapa)


# Mostrar el mapa en pantalla
mapa
