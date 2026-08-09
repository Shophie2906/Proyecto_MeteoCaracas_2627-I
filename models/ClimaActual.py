from datetime import datetime

class ClimaActual:
    """Clase que representa el reporte meteorológico en tiempo real de una localidad."""

    def __init__(self, temperatura, humedad, velocidad_viento, codigo_wmo):
        # Guardamos la temperatura actual recibida de la API (°C)
        self.temperatura = temperatura
        
        # Guardamos el porcentaje de humedad relativa (%)
        self.humedad = humedad
        
        # Guardamos la velocidad del viento (km/h)
        self.velocidad_viento = velocidad_viento
        
        # Código numérico estandarizado que devuelve Open-Meteo para el estado del tiempo
        self.codigo_wmo = codigo_wmo
        
        # Registramos automáticamente la fecha y hora exacta en que se generó este reporte
        self.fecha_hora = datetime.now()

    def obtener_estado_texto(self):
        """Mapea el código numérico WMO de la API a una descripción en español."""
        # Diccionario de equivalencias según la documentación oficial de WMO / Open-Meteo
        codigos = {
            0: "Cielo Despejado",
            1: "Parcialmente Nublado",
            2: "Niebla",
            3: "Llovizna",
            4: "Lluvia",
            5: "Nevada",
            6: "Aguacero",
            7: "Tormenta eléctrica"
        }
        # .get() busca la clave en el diccionario; si no la encuentra, retorna "Desconocido"
        return codigos.get(self.codigo_wmo, "Desconocido")

    def mostrar_reporte_corto(self):
        """Imprime un resumen legible de las condiciones climáticas."""
        # Obtenemos la traducción en texto del código WMO
        estado = self.obtener_estado_texto()
        
        # Imprimimos en consola los valores formateados
        print(f"Estado: {estado} | Temp: {self.temperatura}°C | Humedad: {self.humedad}% | Viento: {self.velocidad_viento} km/h")