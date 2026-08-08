

class RegistroHistorico:
    def __init__(self, mes, anio, temperatura, humedad, precipitacion, velocidad_viento):
        self.mes = mes
        self.anio = anio
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.velocidad_viento = velocidad_viento
        
    def obtener_nombre_mes(self):
        return self.mes.strip().capitalize()
    
    def _str_(self):
        mes_limpio = self.obtener_nombre_mes()
        print(f" [{mes_limpio}{self.anio}] - Temperatura: {self.temperatura}°C | Humedad: {self.humedad}%")
        print(f"           | Precipitacion: {self.precipitacion} mm | Viento: {self.velocidad_viento}km/h")
        
        