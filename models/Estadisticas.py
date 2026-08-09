class Estadisticas:

    def __init__(self):
        pass

    def calcular_promedio_temperatura(self, consultas_sesion: list) -> float:
        if not consultas_sesion:
            return 0.0

        total_temperatura = 0.0
        conteo_validos = 0

        for loc in consultas_sesion:
            if hasattr(loc, 'clima_actual') and loc.clima_actual is not None:
                total_temperatura += loc.clima_actual.temperatura
                conteo_validos += 1

        if conteo_validos == 0:
            return 0.0

        return round(total_temperatura / conteo_validos, 2)

    def obtener_mas_calida(self, consultas_sesion: list):
        validas = [loc for loc in consultas_sesion if getattr(loc, 'clima_actual', None) is not None]
        return max(validas, key=lambda l: l.clima_actual.temperatura) if validas else None

    def obtener_mas_fria(self, consultas_sesion: list):
        validas = [loc for loc in consultas_sesion if getattr(loc, 'clima_actual', None) is not None]
        return min(validas, key=lambda l: l.clima_actual.temperatura) if validas else None