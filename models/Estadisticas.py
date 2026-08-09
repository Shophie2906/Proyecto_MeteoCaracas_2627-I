class Estadisticas:
    """Clase para agrupar promedios y métricas calculadas."""

    def __init__(self, promedio_temperatura, promedio_humedad, total_precipitacion, promedio_viento):
        self.promedio_temperatura = promedio_temperatura
        self.promedio_humedad = promedio_humedad
        self.total_precipitacion = total_precipitacion
        self.promedio_viento = promedio_viento