

class Localidad:
    def __init__(self, nombre, latitud=None, longitud=None):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        
    def show(self):
        print(f" Nombre: {self.nombre}")
        print()

    def tiene_coordenadas(self) -> bool:
        return self.latitud is not None and self.longitud is not None

    def __str__(self) -> str:
        coord_status = f"({self.latitud}, {self.longitud})" if self.tiene_coordenadas() else "(Sin coordenadas)"
        return f"Localidad: {self.nombre} {coord_status}"