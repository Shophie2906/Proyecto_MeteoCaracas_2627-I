from datetime import datetime

class ReporteClima:
    def __init__(self, temperatura, humedad, presion, precipitacion, velocidad_viento=0.0, estado_wmo="Desconocido"):
        self.fecha_hora = datetime.now()
        self.temperatura = temperatura
        self.humedad = humedad
        self.presion = presion
        self.precipitacion = precipitacion
        self.velocidad_viento = velocidad_viento
        self.estado_wmo = estado_wmo  

    def __str__(self):
        fecha_fmt = self.fecha_hora.strftime("%Y-%m-%d %H:%M")
        return (f"[{fecha_fmt}] Temp: {self.temperatura}°C | Hum: {self.humedad}% | "
                f"Presión: {self.presion}hPa | Lluvia: {self.precipitacion}mm | "
                f"Viento: {self.velocidad_viento}km/h | Estado: {self.estado_wmo}")


class Localidad:
    def __init__(self, nombre, latitud=None, longitud=None):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.reportes = []  # Lista de objetos ReporteClima asociados a esta localidad

    def tiene_coordenadas(self):
        return self.latitud is not None and self.longitud is not None

    def agregar_reporte(self, reporte):
        if isinstance(reporte, ReporteClima):
            self.reportes.append(reporte)

    def obtener_ultimo_reporte(self):
        if self.reportes:
            return self.reportes[-1]
        return None

    def __str__(self):
        coord_status = f"({self.latitud}, {self.longitud})" if self.tiene_coordenadas() else "(Sin coordenadas)"
        return f"Localidad: {self.nombre} {coord_status}"


class Municipio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.localidades = [] 

    def agregar_localidad(self, localidad):
        if isinstance(localidad, Localidad):
            self.localidades.append(localidad)

    def buscar_localidad(self, nombre_localidad):
        for loc in self.localidades:
            if loc.nombre.lower() == nombre_localidad.lower():
                return loc
        return None

    def __str__(self):
        return f"Municipio: {self.nombre} - Total Localidades: {len(self.localidades)}"