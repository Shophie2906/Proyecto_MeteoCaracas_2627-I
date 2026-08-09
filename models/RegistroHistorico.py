class RegistroHistorico:
    """Clase para almacenar consolidados meteorológicos de un período específico."""

    def __init__(self, anio, mes, temperatura, humedad, precipitacion, velocidad_viento):
        """
        Inicializa un registro meteorológico histórico.

        :param anio: int, Año del registro.
        :param mes: str o int, Mes del registro o 'Anual'.
        :param temperatura: float, Temperatura promedio (°C).
        :param humedad: float, Humedad relativa promedio (%).
        :param precipitacion: float, Precipitación acumulada (mm).
        :param velocidad_viento: float, Velocidad del viento promedio (km/h).
        """
        self.anio = anio
        self.mes = mes
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.velocidad_viento = velocidad_viento

    def __repr__(self):
        return f"RegistroHistorico({self.anio}-{self.mes}: {self.temperatura:.1f}°C, {self.precipitacion:.1f}mm)"