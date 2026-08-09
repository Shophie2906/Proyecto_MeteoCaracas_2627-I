class Municipio:
    """Clase que representa un municipio del área metropolitana y sus localidades."""

    def __init__(self, nombre, latitud=None, longitud=None):
        """
        Inicializa un Municipio.

        :param nombre: str, Nombre del municipio.
        :param latitud: float o None, Latitud central.
        :param longitud: float o None, Longitud central.
        """
        self._nombre = nombre
        self._latitud = latitud
        self._longitud = longitud
        self._localidades = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def localidades(self):
        return self._localidades

    def agregar_localidad(self, localidad):
        """
        Agrega un objeto Localidad a la lista del municipio.

        :param localidad: Localidad, Instancia de la clase Localidad.
        """
        self._localidades.append(localidad)

    def obtener_total_localidades(self):
        """Retorna el total de localidades asociadas."""
        return len(self._localidades)

    def obtener_localidades_con_coordenadas(self):
        """Retorna una lista de objetos Localidad que poseen coordenadas registradas."""
        return [loc for loc in self._localidades if loc.tiene_coordenadas()]

    def obtener_localidades_sin_coordenadas(self):
        """Retorna una lista de objetos Localidad que tienen coordenadas null."""
        return [loc for loc in self._localidades if not loc.tiene_coordenadas()]

    def calcular_porcentaje_cobertura(self):
        """Calcula el porcentaje de localidades con coordenadas del municipio."""
        total = self.obtener_total_localidades()
        if total == 0:
            return 0.0
        return (len(self.obtener_localidades_con_coordenadas()) / total) * 100.0

    def __repr__(self):
        return f"Municipio('{self._nombre}', total_localidades={self.obtener_total_localidades()})"