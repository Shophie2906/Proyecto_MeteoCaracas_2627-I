import requests
from models.modelos import ReporteClima

class APIClient:
    """Módulo para consultar la API meteorológica Open-Meteo."""

    WMO_CODES = {
        0: "Despejado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        51: "Llovizna ligera",
        61: "Lluvia moderada",
        80: "Chubascos",
        95: "Tormenta eléctrica"
    }

    @staticmethod
    def obtener_clima_localidad(localidad):
        """
        Consulta la API de Open-Meteo para obtener las variables meteorológicas actuales.
        
        :param localidad: Objeto Localidad a consultar.
        :return: Instancia de ReporteClima o None si falla.
        """
        if not localidad.tiene_coordenadas():
            print(f" La localidad '{localidad.nombre}' no tiene coordenadas geográficas registradas.")
            return None

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "current_weather": True,
            "hourly": "relativehumidity_2m,surface_pressure"
        }

        try:
            respuesta = requests.get(url, params=params, timeout=5)
            
            if respuesta.status_code == 200:
                data = respuesta.json()
                current = data.get("current_weather", {})
                
                # Obtenemos la humedad relativa actual estimada desde el array hourly
                hourly_humidity = data.get("hourly", {}).get("relativehumidity_2m", [65.0])
                humedad_actual = hourly_humidity[0] if hourly_humidity else 65.0

                temp = current.get("temperature", 0.0)
                viento = current.get("windspeed", 0.0)
                wmo_code = current.get("weathercode", 0)
                estado = APIClient.WMO_CODES.get(wmo_code, "Clima Variable")

                reporte = ReporteClima(
                    temperatura=temp,
                    humedad=humedad_actual,
                    presion=1013.25,
                    velocidad_viento=viento,
                    estado_wmo=estado,
                    precipitacion=0.0
                )
                
                localidad.agregar_reporte(reporte)
                return reporte
            else:
                print(f"Error HTTP al consultar la API: {respuesta.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f" Error de conexión a Open-Meteo: {e}")
            return None