from datetime import datetime

class ReporteClima:

    def __init__(self, temperatura, humedad, presion, velocidad_viento, estado_wmo, precipitacion=0.0):
        """
        Inicializa un objeto ReporteClima.
        
        :param temperatura: Temperatura en grados Celsius (°C).
        :param humedad: Humedad relativa en porcentaje (%).
        :param presion: Presión atmosférica en hPa.
        :param velocidad_viento: Velocidad del viento en km/h.
        :param estado_wmo: Descripción del estado del tiempo según código WMO.
        :param precipitacion: Precipitación acumulada en mm.
        """
        self.fecha_hora = datetime.now()
        self.temperatura = temperatura
        self.humedad = humedad
        self.presion = presion
        self.velocidad_viento = velocidad_viento
        self.estado_wmo = estado_wmo
        self.precipitacion = precipitacion

    def __str__(self):
        fecha_fmt = self.fecha_hora.strftime("%Y-%m-%d %H:%M")
        return (f"[{fecha_fmt}] Temp: {self.temperatura}°C | Humedad: {self.humedad}% | "
                f"Viento: {self.velocidad_viento} km/h | Estado: {self.estado_wmo}")


class Localidad:

    def __init__(self, nombre, latitud=None, longitud=None):
        """
        Inicializa una localidad con sus coordenadas geográficas.
        
        :param nombre: Nombre de la localidad.
        :param latitud: Latitud en grados decimales o None.
        :param longitud: Longitud en grados decimales o None.
        """
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.reportes = []  # Lista de objetos ReporteClima

    def tiene_coordenadas(self):
        """
        Verifica si la localidad posee coordenadas geográficas válidas.
        
        :return: True si latitud y longitud no son None, False en caso contrario.
        """
        return self.latitud is not None and self.longitud is not None

    def agregar_reporte(self, reporte):
        """
        Agrega un reporte meteorológico al historial de la localidad.
        
        :param reporte: Instancia de la clase ReporteClima.
        """
        self.reportes.append(reporte)

    def __str__(self):
        coords = f"({self.latitud}, {self.longitud})" if self.tiene_coordenadas() else "[Sin Coordenadas]"
        return f"{self.nombre} {coords}"


class Municipio:

    def __init__(self, nombre):
        """
        Inicializa un municipio con su nombre.
        
        :param nombre: Nombre del municipio.
        """
        self.nombre = nombre
        self.localidades = []  # Lista de objetos Localidad

    def agregar_localidad(self, localidad):
        """
        Agrega una localidad al municipio.
        
        :param localidad: Instancia de la clase Localidad.
        """
        self.localidades.append(localidad)

    def obtener_localidades_con_coords(self):
        """
        Retorna únicamente las localidades que tienen coordenadas válidas.
        
        :return: Lista de objetos Localidad con coordenadas.
        """
        return [loc for loc in self.localidades if loc.tiene_coordenadas()]

    def obtener_localidades_sin_coords(self):
        """
        Retorna únicamente las localidades que no tienen coordenadas (null).
        
        :return: Lista de objetos Localidad sin coordenadas.
        """
        return [loc for loc in self.localidades if not loc.tiene_coordenadas()]

    def buscar_localidad_parcial(self, texto_busqueda):
        """
        Busca localidades que coincidan parcialmente con el texto ingresado.
        
        :param texto_busqueda: Cadena de texto a buscar.
        :return: Lista de objetos Localidad que coinciden.
        """
        texto = texto_busqueda.lower().strip()
        return [loc for loc in self.localidades if texto in loc.nombre.lower()]

    def __str__(self):
        return f"Municipio: {self.nombre} ({len(self.localidades)} localidades)"