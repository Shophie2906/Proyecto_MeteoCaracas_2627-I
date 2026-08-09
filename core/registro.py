from datetime import datetime
from models.RegistroHistorico import RegistroHistorico
class RegistroController:
    """Gestiona el flujo de registro histórico y almacenamiento de lecturas."""

    def __init__(self):
        self.historico = []

    def registrar_lectura(self, municipio, clima):
        """ Toma un municipio y su ClimaActual e instancia un RegistroHistorico"""
        ahora = datetime.now()
        registro = RegistroHistorico(
            mes=ahora.strftime("%B"),
            anio=ahora.year,
            temperatura=clima.temperatura,
            humedad=clima.humedad,
            precipitacion=clima.precipitacion,
            velocidad_viento=clima.velocidad_viento
        )
        self.historico.append({
            "municipio": municipio.nombre,
            "fecha": ahora.strftime("%Y-%m-%d %H:%M:%S"),
            "datos": registro.__dict__
        })
        return registro

    def obtener_todos(self):
        return self.historico