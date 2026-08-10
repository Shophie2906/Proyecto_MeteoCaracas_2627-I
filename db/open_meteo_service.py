import requests

class OpenMeteoService:
    """Servicio de conexión e interacción HTTP con las APIs públicas de Open-Meteo."""

    BASE_URL_FORECAST = "https://api.open-meteo.com/v1/forecast"
    BASE_URL_ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"

    @staticmethod
    def obtener_clima_actual(latitud, longitud):
        """
        Consulta las condiciones climatológicas en tiempo real para una coordenada dada.

        :param latitud: Latitud geográfica (float).
        :param longitud: Longitud geográfica (float).
        :return: Tupla con (temperatura, humedad, velocidad_viento, codigo_wmo) o None si falla.
        """
        params = {
            "latitude": latitud,
            "longitude": longitud,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"]
        }

        try:
            response = requests.get(OpenMeteoService.BASE_URL_FORECAST, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            current = data.get("current", {})
            if current:
                temp = current.get("temperature_2m", 0.0)
                hum = current.get("relative_humidity_2m", 0)
                viento = current.get("wind_speed_10m", 0.0)
                wmo = current.get("weather_code", 0)
                return (temp, hum, viento, wmo)
            
            # Respaldo si usa la versión clásica current_weather
            current_w = data.get("current_weather", {})
            if current_w:
                temp = current_w.get("temperature", 0.0)
                hum = 60  # Valor por defecto si no es provisto en la respuesta clásica
                viento = current_w.get("windspeed", 0.0)
                wmo = current_w.get("weathercode", 0)
                return (temp, hum, viento, wmo)

            return None

        except requests.RequestException as e:
            print(f"Error de comunicación con Open-Meteo API: {e}")
            return None

    @staticmethod
    def obtener_datos_historicos(latitud, longitud, fecha_inicio, fecha_fin):
        """
        Consulta registros históricos meteorológicos entre dos fechas (AAAA-MM-DD).

        :param latitud: Latitud de la localidad (float).
        :param longitud: Longitud de la localidad (float).
        :param fecha_inicio: Fecha inicial en formato YYYY-MM-DD.
        :param fecha_fin: Fecha final en formato YYYY-MM-DD.
        :return: Diccionario con listas de métricas (time, temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m) o None.
        """
        params = {
            "latitude": latitud,
            "longitude": longitud,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"]
        }

        # Intentamos en el endpoint de archivo histórico primero, y si no en el de forecast
        urls = [OpenMeteoService.BASE_URL_ARCHIVE, OpenMeteoService.BASE_URL_FORECAST]

        for url in urls:
            try:
                response = requests.get(url, params=params, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if "hourly" in data:
                        return data["hourly"]
            except requests.RequestException:
                continue

        print("Error: No se pudieron obtener los datos históricos de Open-Meteo.")
        return None
