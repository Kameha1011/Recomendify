CANCION = "Cancion"
USUARIO = "Usuario"

class Vertice:
    def __init__(self, nombre):
        self._nombre = nombre

    def __repr__(self):
        return f"Vertice({self._nombre})"

    def __eq__(self, other):
        # Comparar vértices por su _nombre
        return isinstance(other, Vertice) and self._nombre == other._nombre

    def __hash__(self):
        # Usar el nombre para calcular el hash
        return hash(self._nombre)

    def nombre(self):
        return self._nombre

class Cancion(Vertice):
    def __init__(self, nombre_cancion,nombre_artista):
        super().__init__(f"{self.nombre_cancion} - {self.nombre_artista}")
        self.nombre_cancion = nombre_cancion
        self.nombre_artista = nombre_artista
        self.tipo = CANCION

    def __str__(self):
        return f"{self.nombre_cancion} - {self.nombre_artista}"

class Usuario(Vertice):
    def __init__(self, id_usuario):
        super().__init__(id_usuario)
        self.id_usuario = id_usuario
        self.tipo = USUARIO

    def __str__(self):
        return self.id_usuario

class Playlist_Usuario:
    def __init__(self):
        self.playlists = {}

    def agregar_playlist(self, nombre_playlist, id_playlist):
        self.playlists[id_playlist] = nombre_playlist
