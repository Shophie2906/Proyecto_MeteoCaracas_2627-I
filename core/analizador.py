class AnalizadorDatos:
    
    def calcular_promedio_temperatura(registros):
        if not registros:
            return 0.0
        suma = sum(r.temperatura for r in registros)
        return round(suma / len(registros), 2)

    def obtener_temperatura_maxima(registros):
        if not registros:
            return None
        return max(r.temperatura for r in registros)

    def obtener_temperatura_minima(registros):
        if not registros:
            return None
        return min(r.temperatura for r in registros)

    def calcular_lluvia_total(registros):
        if not registros:
            return 0.0
        return round(sum(r.lluvia for r in registros), 2)