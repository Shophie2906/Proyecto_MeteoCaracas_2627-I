from Localidad import Localidad

class Municipio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.localidades = [] 

    def agregar_localidad(self, localidad):
        if isinstance(localidad, Localidad):
            self.localidades.append(localidad)

    def buscar_localidad(self, nombre_localidad):
        for loc in self.localidades:
            if loc.nombre.lower() == nombre_localidad.lower():
                return loc
        return None
    
    def total_localidades(self):
        return len(self.localidades)
    
    def localidades_con_coordenadas(self):
        return [loc for loc in self.localidades if loc.tiene_coordenadas()]
    
    def porcentaje_con_coordenadas(self):
        total = self.total_localidades()
        if total == 0:
            return 0.0 
        return round((len(self.localidades_con_coordenadas()) / total)* 100, 2)
    
    def __str__(self):
        return f"Municipio: {self.nombre} - Total Localidades: {self.total_localidades()}"