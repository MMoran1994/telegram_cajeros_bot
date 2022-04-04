import auxiliares
from sklearn.neighbors import BallTree

class RedDeCajeros:
    def __init__(self, dataset):
        self.dataset = dataset
        coords_en_radianes = self.__obtener_coordenadas_en_radianes(dataset)
        self.arbol_de_coordenadas = BallTree(coords_en_radianes, metric='haversine')

    def k_mas_cercanos(self, coordenada, k):
        coor_en_radianes = auxiliares.a_radianes(coordenada)

        #Obtener los k cajeros más cercanos a la coordenada
        #Como el árbol está balanceado la búsqueda tiene un costo de O(log(n)) con n la cantidad de coordenadas del dataset
        dists, ii = self.arbol_de_coordenadas.query([coor_en_radianes], k=k, sort_results=False)
        dists = dists[0]
        ii = ii[0]
        dists_en_metros = [dist*6371000 for dist in dists] #multiplicar * 6371 (radio de la tierra) para obtener kms
        cajeros_en_rango = []
        for j in range(0, k):
            cajero = {
                    'id':self.dataset[ii[j]]['id'],
                    'banco':self.dataset[ii[j]]['banco'], 
                    'ubicacion':self.dataset[ii[j]]['ubicacion'],
                    'lat':float(self.dataset[ii[j]]['lat']),
                    'long':float(self.dataset[ii[j]]['long']),
                    'dist_a_us':dists_en_metros[j]}
            cajeros_en_rango.append(cajero)
        return cajeros_en_rango

    def __obtener_coordenadas_en_radianes(self, dataset):
        coords_en_radianes = list()

        for row in dataset:
            coord_actual=auxiliares.a_radianes((row["lat"], row["long"]))
            coords_en_radianes.append(coord_actual)
        return coords_en_radianes