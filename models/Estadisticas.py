from ClimaActual import ClimaActual

class Estadisticas:
    def __init__(self):
        pass
        
    def calcular_promedio_temperatura(self, consultas_sesion):
        if not consultas_sesion:
            return 0.0
        total_temperatura = 0.0
        for loc in consultas_sesion:
            if loc.clima_actual:
                total_temperatura += loc.clima_actual.temperatura
        return total_temperatura / len(consultas_sesion)
    
    
    