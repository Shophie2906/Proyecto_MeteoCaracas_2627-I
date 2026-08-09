from core.api_client import APIClient
from core.modelos import LecturaMeteorologica, Municipio
class GestorConsultas:
    """Maneja las operaciones de búsqueda y consulta de datos meteorológicos guardando el historial de la sesión activa en listas de objetos."""

    def __init__(self, municipios: list[Municipio]):
        self.municipios = municipios
        self.historial_sesion: list[LecturaMeteorologica] = []

    def buscar_localidad_por_nombre(self, nombre_buscado: str):
        """Busca una localidad en todos los municipios por coincidencia de nombre.

        Returns:
            tuple (Localidad, str) o (None, None)"""
        nombre_limpio = nombre_buscado.strip().lower()
        for municipio in self.municipios:
            for localidad in municipio.localidades:
                if localidad.nombre.lower() == nombre_limpio:
                    return localidad, municipio.nombre
        return None, None

    def consultar_por_busqueda_directa(
        self, nombre_localidad: str
    ) -> LecturaMeteorologica | None:
        """Realiza la búsqueda directa por texto e invoca la API si existe la localidad."""
        localidad, municipio_nombre = self.buscar_localidad_por_nombre(
            nombre_localidad
        )

        if not localidad:
            print(
                f" No se encontró la localidad '{nombre_localidad}' en la base de datos."
            )
            return None

        lectura = APIClient.obtener_clima_actual(localidad, municipio_nombre)
        if lectura:
            self.historial_sesion.append(lectura)
        return lectura

    def consultar_por_seleccion(
        self, municipio_nombre: str, localidad_nombre: str
    ) -> LecturaMeteorologica | None:
        """Consulta la API seleccionando municipio y localidad de la lista cargada."""
        municipio = next(
            (m for m in self.municipios if m.nombre == municipio_nombre), None
        )
        if not municipio:
            print(f" Municipio '{municipio_nombre}' no encontrado.")
            return None

        localidad = next(
            (l for l in municipio.localidades if l.nombre == localidad_nombre),
            None,
        )
        if not localidad:
            print(
                f"Localidad '{localidad_nombre}' no encontrada en {municipio_nombre}."
            )
            return None

        lectura = APIClient.obtener_clima_actual(localidad, municipio.nombre)
        if lectura:
            self.historial_sesion.append(lectura)
        return lectura