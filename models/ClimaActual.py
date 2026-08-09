from datetime import datetime

class ClimaActual:

    def __init__(self, temperatura: float, humedad: float, velocidad_viento: float, codigo_wmo: int):
        """
        Inicializa un reporte de clima actual.
        
        :param temperatura: Temperatura actual en °C.
        :param humedad: Humedad relativa en %.
        :param velocidad_viento: Velocidad del viento en km/h.
        :param codigo_wmo: Código numérico de estado según WMO.
        """
        self.temperatura = temperatura
        self.humedad = humedad
        self.velocidad_viento = velocidad_viento
        self.codigo_wmo = codigo_wmo
        self.fecha_hora = datetime.now()

    def obtener_estado_texto(self) -> str:
    
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
        return codigos.get(self.codigo_wmo, "Desconocido")

    def mostrar_reporte_corto(self) -> None:
        estado = self.obtener_estado_texto()
        print(f"Estado: {estado} | Temp: {self.temperatura}°C | Humedad: {self.humedad}% | Viento: {self.velocidad_viento} km/h")