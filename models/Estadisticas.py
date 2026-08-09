class Estadisticas:
    """Clase encargada de realizar cálculos analíticos sobre las consultas de la sesión."""

    def __init__(self):
        pass

    def calcular_promedio_temperatura(self, consultas_sesion):
        """Calcula la temperatura promedio global de las consultas realizadas en la sesión."""
        # Si la lista de consultas está vacía, retornamos 0.0 inmediatamente
        if not consultas_sesion:
            return 0.0

        total_temperatura = 0.0
        conteo_validos = 0

        # Recorremos cada localidad consultada durante la sesión activa
        for loc in consultas_sesion:
            # Verificamos que la localidad tenga asignado un objeto clima_actual no nulo
            if hasattr(loc, 'clima_actual') and loc.clima_actual is not None:
                total_temperatura += loc.clima_actual.temperatura
                conteo_validos += 1  # Incrementamos solo si aportó una temperatura real

        # Si ninguna localidad tenía clima válido, evitamos división por cero
        if conteo_validos == 0:
            return 0.0

        # Dividimos el acumulador exclusivamente entre el conteo real de registros válidos
        return round(total_temperatura / conteo_validos, 2)

    def obtener_mas_calida(self, consultas_sesion):
        """Identifica y devuelve la localidad consultada con la mayor temperatura (Ranking)."""
        # Filtramos primero la lista asegurando que tengan clima_actual asignado
        validas = [loc for loc in consultas_sesion if getattr(loc, 'clima_actual', None) is not None]
        # Usamos max() con una función lambda que extrae la temperatura de cada objeto
        return max(validas, key=lambda l: l.clima_actual.temperatura) if validas else None

    def obtener_mas_fria(self, consultas_sesion):
        """Identifica y devuelve la localidad consultada con la menor temperatura (Ranking)."""
        # Filtramos primero la lista asegurando que tengan clima_actual asignado
        validas = [loc for loc in consultas_sesion if getattr(loc, 'clima_actual', None) is not None]
        # Usamos min() con una función lambda que extrae la temperatura de cada objeto
        return min(validas, key=lambda l: l.clima_actual.temperatura) if validas else None