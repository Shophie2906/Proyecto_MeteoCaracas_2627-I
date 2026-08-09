import requests
from core.modelos import LecturaMeteorologica, Localidad
class APIClient:
    """Clase estática encargada del consumo de servicios web meteorológicos utilizando la librería requests."""

    URL_TIEMPO_REAL = "https://api.open-meteo.com/v1/forecast"

    @classmethod
    def obtener_clima_actual(
        cls, localidad: Localidad, municipio_nombre: str
    ) -> LecturaMeteorologica | None:
        """Consulta los parámetros meteorológicos actuales de una localidad a través de sus coordenadas geográficas.

        Args:
            localidad (Localidad): Objeto localidad a consultar.
            municipio_nombre (str): Nombre del municipio perteneciente.

        Returns:
            LecturaMeteorologica | None: Objeto con la lectura capturada o None si falla la consulta o faltan coordenadas."""
        if not localidad.tiene_coordenadas():
            print(
                f" Error: La localidad '{localidad.nombre}' no tiene coordenadas válidas registradas."
            )
            return None

        params = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m",
                "precipitation",
            ],
            "timezone": "auto",
        }

        try:
            respuesta = requests.get(
                cls.URL_TIEMPO_REAL, params=params, timeout=10
            )
            respuesta.raise_for_status()
            datos = respuesta.json()

            actual = datos.get("current", {})

            return LecturaMeteorologica(
                localidad_nombre=localidad.nombre,
                municipio_nombre=municipio_nombre,
                temperatura=actual.get("temperature_2m", 0.0),
                humedad=actual.get("relative_humidity_2m", 0.0),
                viento=actual.get("wind_speed_10m", 0.0),
                precipitacion=actual.get("precipitation", 0.0),
            )

        except requests.exceptions.RequestException as e:
            print(
                f" Error al consultar la API para '{localidad.nombre}': {e}"
            )
            return None
        # Agregar a core/api_client.py
class APIClient:
    # ... código anterior ...
    URL_HISTORICO = "https://archive-api.open-meteo.com/v1/archive"

    @classmethod
    def obtener_historial_diario(
        cls, localidad: Localidad, fecha_inicio: str, fecha_fin: str
    ) -> dict | None:
        """Consulta datos históricos diarios para una localidad en un rango de fechas.

        Args:
            localidad (Localidad): Objeto localidad con coordenadas.
            fecha_inicio (str): Fecha de inicio en formato 'YYYY-MM-DD'.
            fecha_fin (str): Fecha final en formato 'YYYY-MM-DD'.

        Returns:
            dict | None: Diccionario con la respuesta de la API o None si falla.
        """
        if not localidad.tiene_coordenadas():
            print(
                f" Error: La localidad '{localidad.nombre}' no tiene coordenadas."
            )
            return None

        params = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
                "relative_humidity_2m_mean",
                "precipitation_sum",
                "wind_speed_10m_max",
            ],
            "timezone": "auto",
        }

        try:
            respuesta = requests.get(
                cls.URL_HISTORICO, params=params, timeout=15
            )
            respuesta.raise_for_status()
            return respuesta.json()
        except requests.exceptions.RequestException as e:
            print(f" Error al consultar el historial meteorológico: {e}")
            return None