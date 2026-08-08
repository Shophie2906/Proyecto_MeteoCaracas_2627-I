from datetime import datetime
from Localidad import Localidad

class ClimaActual:
    def __init__(self, temperatura, humedad, velocidad_viento, codigo_wmo):
        self.temperatura = temperatura                          
        self.velocidad_viento = velocidad_viento 
        self.codigo_wmo = codigo_wmo
        self.fecha_hora = datetime.now()
        
    def obtener_estado_texto(self): 
        # Traducir el codigo numerico de la api 
        if self.codigo_wmo == 0:
            print("Cielo Despejado")
        elif self.codigo_wmo == 1:
            print("Parcialmente Nublado")
        elif self.codigo_wmo == 2:
            print("Niebla")
        elif self.codigo_wmo == 3:
            print("Llovizna")  
        elif self.codigo_wmo == 4:
            print("Lluvia")
        elif self.codigo_wmo == 5:
            print("Nevada")
        elif self.codigo_wmo == 6:
            print("Aguacero")
        elif self.codigo_wmo == 7:
            print("Tormenta electrica")
        else: 
            print("Desconocido")  
            
    def mostrar_resporte_corto(self):
        estado = self.obtener_estado_texto()
        print(f" Temperatura: {self.temperatura}°C | Viento: {self.velocidad_viento} km/h")    
        
        
        