class RegistroHistorico:
    """Clase que representa el resumen meteorológico mensual de una localidad para análisis histórico."""

    def __init__(self, mes, anio, temperatura, humedad, precipitacion, velocidad_viento):
        # Nombre del mes (ej. "Enero", "Febrero")
        self.mes = mes
        
        # Año del registro (int, ej. 2023)
        self.anio = anio
        
        # Temperatura promedio mensual (°C)
        self.temperatura = temperatura
        
        # Humedad relativa promedio mensual (%)
        self.humedad = humedad
        
        # Precipitación acumulada mensual (mm)
        self.precipitacion = precipitacion
        
        # Velocidad promedio del viento (km/h)
        self.velocidad_viento = velocidad_viento

    def obtener_nombre_mes(self):
        """Retorna el nombre del mes asociado al registro histórico."""
        return str(self.mes)

    def mostrar_resumen_mensual(self):
        """Imprime un resumen formateado de las métricas registradas en el mes."""
        print(f"🗓️ {self.mes} {self.anio} | Temp Prom: {self.temperatura}°C | Hum: {self.humedad}% | Prec: {self.precipitacion}mm | Viento: {self.velocidad_viento} km/h")

    def __str__(self):
        """Representación formal en texto del registro histórico."""
        return f"RegistroHistorico({self.mes} {self.anio} - Temp: {self.temperatura}°C, Prec: {self.precipitacion}mm)"