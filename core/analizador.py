from models.Estadisticas import Estadisticas

class AnalizadorClima:
    """Genera estadísticas a partir de conjuntos de lecturas."""

    @staticmethod
    def calcular_estadisticas_mes(registros_historicos, mes, anio):
        """Filtra lecturas por mes/año y calcula promedios/totales."""
        filtrados = [
            r for r in registros_historicos 
            if r.mes.lower() == mes.lower() and r.anio == anio
        ]

        if not filtrados:
            return None

        total_temp = sum(r.temperatura for r in filtrados)
        total_hum = sum(r.humedad for r in filtrados)
        total_prec = sum(r.precipitacion for r in filtrados)
        total_viento = sum(r.velocidad_viento for r in filtrados)
        n = len(filtrados)

        return Estadisticas(
            promedio_temperatura=total_temp / n,
            promedio_humedad=total_hum / n,
            total_precipitacion=total_prec,
            promedio_viento=total_viento / n
        )