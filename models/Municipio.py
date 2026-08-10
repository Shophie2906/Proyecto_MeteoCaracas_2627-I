# Importamos la clase Localidad que está en la misma carpeta models/
from .Localidad import Localidad

class Municipio:
    """Clase contenedora que agrupa y administra las localidades de un municipio."""

    def __init__(self, nombre):
        # Nombre del municipio (ej. "Chacao", "Sucre")
        self.nombre = nombre
        
        # Lista donde guardaremos los objetos de tipo Localidad pertenecientes a este municipio
        self.localidades = []

    def agregar_localidad(self, localidad):
        """Añade una localidad a la lista tras validar que sea del tipo correcto."""
        # Validación de seguridad orientada a objetos (evita meter datos corruptos)
        if isinstance(localidad, Localidad):
            self.localidades.append(localidad)

    def buscar_localidad(self, nombre_localidad):
        """Búsqueda exacta por nombre (sin importar mayúsculas/minúsculas)."""
        for loc in self.localidades:
            # Comparamos ambos textos pasados a minúsculas (.lower())
            if loc.nombre.lower() == nombre_localidad.lower():
                return loc  # Retorna el objeto si lo encuentra
        return None  # Retorna None si no hubo coincidencia

    def buscar_localidades_parcial(self, texto_busqueda):
        """Búsqueda por coincidencia parcial (Requerimiento 2.b)."""
        # Limpiamos espacios alrededor (.strip()) y pasamos a minúsculas
        texto = texto_busqueda.lower().strip()
        # Comprensión de listas: filtra las localidades cuyo nombre contenga el texto buscado
        return [loc for loc in self.localidades if texto in loc.nombre.lower()]

    def total_localidades(self):
        """Retorna el conteo total de localidades en el municipio."""
        return len(self.localidades)

    def localidades_con_coordenadas(self):
        """Retorna una lista filtrada solo con las localidades que TIENEN coordenadas."""
        return [loc for loc in self.localidades if loc.tiene_coordenadas()]

    def localidades_sin_coordenadas(self):
        """Retorna una lista filtrada solo con las localidades que NO tienen coordenadas (NULL)."""
        return [loc for loc in self.localidades if not loc.tiene_coordenadas()]

    def porcentaje_con_coordenadas(self):
        """Calcula el porcentaje de cobertura territorial con coordenadas (Métrica D)."""
        total = self.total_localidades()
        # Evitamos la división por cero si el municipio no tiene localidades
        if total == 0:
            return 0.0 
        # Fórmula: (Localidades con Coordenadas / Total Localidades) * 100, redondeado a 2 decimales
        return round((len(self.localidades_con_coordenadas()) / total) * 100, 2)

    def __str__(self):
        """Representación en texto del objeto Municipio."""
        return f"Municipio: {self.nombre} - Total Localidades: {self.total_localidades()}"