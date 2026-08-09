from datetime import datetime
class LecturaMeteorologica:
    """Representa una lectura meteorológica capturada en tiempo real o histórica, y guarda las magnitudes consultadas para una localidad específica."""

    def __init__(
        self,
        localidad_nombre: str,
        municipio_nombre: str,
        temperatura: float,
        humedad: float,
        viento: float,
        precipitacion: float,
        fecha_hora: str = None,
    ):
        self.localidad_nombre = localidad_nombre
        self.municipio_nombre = municipio_nombre
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.precipitacion = precipitacion
        self.fecha_hora = fecha_hora or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def __str__(self) -> str:
        return (
            f"[{self.fecha_hora}] {self.localidad_nombre} ({self.municipio_nombre}): "
            f"{self.temperatura}°C, Humedad: {self.humedad}%, Viento: {self.viento} km/h, "
            f"Precipitación: {self.precipitacion} mm"
        )