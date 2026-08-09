import requests
from models.ClimaActual import ClimaActual

class APIClient:
    """Cliente para consumir la API pública de Open-Meteo."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def obtener_clima_actual_batch(lista_municipios):
        """
        Solicita el clima actual para una lista de objetos Municipio.
        Construye la URL múltiple con latitudes y longitudes agrupadas.
        """
        if not lista_municipios:
            return []

        latitudes = ",".join(str(m.latitud) for m in lista_municipios)
        longitudes = ",".join(str(m.longitud) for m in lista_municipios)

        params = {
            "latitude": latitudes,
            "longitude": longitudes,
            "current_weather": True
        }

        try:
            response = requests.get(APIClient.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Si es una lista de resultados (múltiples coordenadas)
            if isinstance(data, list):
                resultados = []
                for i, item in enumerate(data):
                    current = item.get("current_weather", {})
                    clima = ClimaActual(
                        temperatura=current.get("temperature", 0.0),
                        humedad=current.get("relative_humidity", 0.0), # Si la API lo envía
                        precipitacion=current.get("precipitation", 0.0),
                        velocidad_viento=current.get("windspeed", 0.0)
                    )
                    resultados.append((lista_municipios[i], clima))
                return resultados
            else:
                # Caso de un solo municipio devuelto como objeto único
                current = data.get("current_weather", {})
                clima = ClimaActual(
                    temperatura=current.get("temperature", 0.0),
                    humedad=current.get("relative_humidity", 0.0),
                    precipitacion=current.get("precipitation", 0.0),
                    velocidad_viento=current.get("windspeed", 0.0)
                )
                return [(lista_municipios[0], clima)]

        except requests.RequestException as e:
            print(f"Error al conectar con la API de Open-Meteo: {e}")
            return []