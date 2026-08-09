class RegistroHistorico:

    def __init__(self, mes: str, anio: int, temperatura: float, humedad: float, precipitacion: float, velocidad_viento: float):
        self.mes = mes
        self.anio = anio
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.velocidad_viento = velocidad_viento

    def obtener_nombre_mes(self) -> str:
        if isinstance(self.mes, str):
            return self.mes.strip().capitalize()
        return str(self.mes)

    def __str__(self) -> str:
        mes_limpio = self.obtener_nombre_mes()
        return (f"[{mes_limpio} {self.anio}] - Temp: {self.temperatura}°C | Humedad: {self.humedad}%\n"
                f"            | Precipitación: {self.precipitacion} mm | Viento: {self.velocidad_viento} km/h")