class Localidad:
    """Clase que representa una localidad geográfica perteneciente a un municipio."""

    def __init__(self, nombre, latitud=None, longitud=None):
        """
        Inicializa un objeto Localidad.

        :param nombre: str, Nombre de la localidad.
        :param latitud: float o None, Coordenada de latitud.
        :param longitud: float o None, Coordenada de longitud.
        """
        self._nombre = nombre
        self._latitud = latitud
        self._longitud = longitud

    @property
    def nombre(self):
        """Obtiene el nombre de la localidad."""
        return self._nombre

    @property
    def latitud(self):
        """Obtiene la latitud de la localidad."""
        return self._latitud

    @property
    def longitud(self):
        """Obtiene la longitud de la localidad."""
        return self._longitud

    def tiene_coordenadas(self):
        """
        Verifica si la localidad posee coordenadas geográficas conocidas (no null).

        :return: bool, True si posee latitud y longitud válidas, False en caso contrario.
        """
        return self._latitud is not None and self._longitud is not None

    def __repr__(self):
        estado_coord = f"({self._latitud}, {self._longitud})" if self.tiene_coordenadas() else "(sin coordenadas)"
        return f"Localidad('{self._nombre}', {estado_coord})"