class RegistroHistorico:
    """Clase que representa una medición mensual consolidada en las consultas de históricos."""

    def __init__(self, mes, anio, temperatura, humedad, precipitacion, velocidad_viento):
        # Nombre o número del mes del registro
        self.mes = mes
        
        # Año correspondiente (int)
        self.anio = anio
        
        # Promedio de temperatura registrada en ese mes (°C)
        self.temperatura = temperatura
        
        # Promedio de humedad relativa (%)
        self.humedad = humedad
        
        # Suma o acumulado de precipitaciones (mm)
        self.precipitacion = precipitacion
        
        # Promedio de velocidad del viento (km/h)
        self.velocidad_viento = velocidad_viento

    def obtener_nombre_mes(self):
        """Formatea el nombre del mes para presentarlo de manera limpia."""
        if isinstance(self.mes, str):
            # Quita espacios al inicio/final (.strip()) y pone la inicial en mayúscula (.capitalize())
            return self.mes.strip().capitalize()
        return str(self.mes)

    def __str__(self):
        """Formatea la salida en texto para imprimir cómodamente el registro histórico."""
        mes_limpio = self.obtener_nombre_mes()
        # Retornamos (importante: return, no print) el texto multilínea estructurado
        return (f"[{mes_limpio} {self.anio}] - Temp: {self.temperatura}°C | Humedad: {self.humedad}%\n"
                f"            | Precipitación: {self.precipitacion} mm | Viento: {self.velocidad_viento} km/h")