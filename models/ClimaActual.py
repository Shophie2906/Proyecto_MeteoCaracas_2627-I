class ClimaActual:
    """Clase que encapsula las variables meteorológicas obtenidas en tiempo real."""

    def __init__(self, temperatura, humedad, velocidad_viento, estado_tiempo="Desconocido", precipitacion=0.0):
        """
        Inicializa la lectura climática.

        :param temperatura: float, Temperatura en °C.
        :param humedad: float, Humedad relativa en %.
        :param velocidad_viento: float, Velocidad del viento en km/h.
        :param estado_tiempo: str, Descripción técnica del tiempo (código WMO).
        :param precipitacion: float, Precipitación acumulada.
        """
        self.temperatura = temperatura
        self.humedad = humedad
        self.velocidad_viento = velocidad_viento
        self.estado_tiempo = estado_tiempo
        self.precipitacion = precipitacion

    def __repr__(self):
        return f"ClimaActual({self.temperatura}°C, Hum: {self.humedad}%, Viento: {self.velocidad_viento}km/h, {self.estado_tiempo})"