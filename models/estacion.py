class Registro:
    def __init__(self, fecha, temperatura, humedad, presion, lluvia):
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.presion = presion
        self.lluvia = lluvia

    def a_dict(self):
        return {
            "fecha": self.fecha,
            "temperatura": self.temperatura,
            "humedad": self.humedad,
            "presion": self.presion,
            "lluvia": self.lluvia
        }