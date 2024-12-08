import random

class Grafo:
    def __init__(self, dirigido=False):
        self.grafo = {}
        self.dirigido = dirigido
        self._iter_index = 0
    
    def __str__(self):
        return str(self.grafo)

    def agregar_vertice(self, vertice):
        if vertice not in self.grafo:
            self.grafo[vertice] = {}

    def __existe_vertice__(self, vertice):
        return vertice in self.grafo

    def agregar_arista(self, vertice1, vertice2, peso=1):
        if not self.__existe_vertice__(vertice1) or not self.__existe_vertice__(vertice2):
            raise ValueError("Alguno de los vertices no existe")

        # Agregar la conexión vertice1 -> vertice2
        self.grafo[vertice1][vertice2] = peso

        # Si no es dirigido, también agregamos la conexión inversa
        if not self.dirigido:
            self.grafo[vertice2][vertice1] = peso

    def adyacentes(self, vertice):
        return self.grafo[vertice]

    def obtener_vertice_aleatorio(self):
        return random.choice(list(self.grafo.keys()))
    
    def peso_arista(self, vertice1, vertice2):
        if not self.estan_unidos(vertice1, vertice2):
            raise ValueError("La arista no existe")
        
        return self.grafo[vertice1][vertice2]

    def estan_unidos(self, vertice1, vertice2):
        vertices_existen = self.__existe_vertice__(vertice1) and self.__existe_vertice__(vertice2)
        return vertices_existen and vertice2 in self.grafo[vertice1] 

    def eliminar_arista(self, vertice1, vertice2):
        if not self.estan_unidos(vertice1, vertice2):
            raise ValueError("La arista no existe")
        
        self.grafo[vertice1].pop(vertice2)

        if not self.dirigido:
            self.grafo[vertice2].pop(vertice1)
    
    def eliminar_vertice(self, vertice):
        if not self.__existe_vertice__(vertice):
            raise ValueError("El vertice no existe")
        
        for v in self.grafo:
            if vertice in self.grafo[v]:
                self.grafo[v].pop(vertice)

        self.grafo.pop(vertice)

    def __contains__(self, vertice):
        return vertice in self.grafo
    
    def __iter__(self):
        return iter(self.grafo)
    
    def __len__(self):
        return len(self.grafo)
