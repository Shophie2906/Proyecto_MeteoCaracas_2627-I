from datetime import datetime
class ClimaActual:
    """Clase que representa el reporte meteorológico en tiempo real de una localidad."""

    def __init__(self, temperatura, humedad, velocidad_viento, codigo_wmo):
        self.temperatura = temperatura
        self.humedad = humedad
        self.velocidad_viento = velocidad_viento
        self.codigo_wmo = codigo_wmo
        self.fecha_hora = datetime.now()

    def obtener_estado_texto(self):
        """Mapea el código numérico WMO de la API a una descripción en español."""
        codigos = {
            0: "Cielo Despejado",
            1: "Principalmente Despejado",
            2: "Parcialmente Nublado",
            3: "Nublado",
            45: "Niebla",
            48: "Niebla con escarcha",
            51: "Llovizna ligera",
            53: "Llovizna moderada",
            55: "Llovizna densa",
            61: "Lluvia ligera",
            63: "Lluvia moderada",
            65: "Lluvia fuerte",
            71: "Nevada ligera",
            73: "Nevada moderada",
            75: "Nevada fuerte",
            80: "Chubascos ligeros",
            81: "Chubascos moderados",
            82: "Chubascos violentos",
            95: "Tormenta eléctrica",
            96: "Tormenta eléctrica con granizo ligero",
            99: "Tormenta eléctrica con granizo fuerte"
        }
        return codigos.get(self.codigo_wmo, "Desconocido")

    def mostrar_reporte_corto(self):
        """Imprime un resumen legible de las condiciones climáticas."""
        estado = self.obtener_estado_texto()
        print(f"Estado: {estado} | Temp: {self.temperatura}°C | Humedad: {self.humedad}% | Viento: {self.velocidad_viento} km/h")