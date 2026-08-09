from models.ClimaActual import ClimaActual
from models.Estadisticas import Estadisticas
from db.open_meteo_service import OpenMeteoService

class GestorClima:
    """Controlador que administra las consultas de clima en tiempo real, búsquedas y estadísticas de sesión."""

    def __init__(self, municipios):
        """
        Inicializa el gestor de clima con la lista de municipios cargados.

        :param municipios: Lista de objetos Municipio.
        """
        self.municipios = municipios
        # Lista de objetos Localidad que han sido consultados en la sesión activa
        self.consultas_sesion = []
        # Instancia auxiliar de la clase Estadisticas para cálculos analíticos
        self.estadisticas = Estadisticas()

    def consultar_clima_localidad(self, localidad, municipio=None):
        """
        Realiza la consulta en tiempo real a Open-Meteo para una localidad dada,
        instancia un objeto ClimaActual y lo asocia a la localidad.

        :param localidad: Instancia de Localidad a consultar.
        :param municipio: Instancia opcional de Municipio al que pertenece.
        :return: Instancia de ClimaActual creada o None si la consulta falla.
        """
        if not localidad.tiene_coordenadas():
            print(f"Error: La localidad '{localidad.nombre}' no tiene coordenadas geográficas registradas.")
            return None

        # Llamada al servicio HTTP en la capa db
        datos = OpenMeteoService.obtener_clima_actual(localidad.latitud, localidad.longitud)
        if not datos:
            print(f"No se pudo consultar el clima para '{localidad.nombre}'. Verifique la conexión.")
            return None

        temp, humedad, viento, codigo_wmo = datos
        # Instanciamos estrictamente el objeto ClimaActual (POO)
        clima = ClimaActual(
            temperatura=temp,
            humedad=humedad,
            velocidad_viento=viento,
            codigo_wmo=codigo_wmo
        )

        # Asociamos la propiedad al objeto localidad
        localidad.clima_actual = clima

        # Registramos en la lista de consultas de la sesión
        self.consultas_sesion.append(localidad)

        return clima

    def buscar_localidades_por_nombre(self, termino):
        """
        Busca localidades que coincidan parcialmente con el término ingresado
        y que posean coordenadas geográficas válidas.

        :param termino: Cadena de texto a buscar.
        :return: Lista de tuplas (Municipio, Localidad).
        """
        texto = termino.strip().lower()
        if not texto:
            return []

        coincidencias = []
        for mun in self.municipios:
            for loc in mun.localidades_con_coordenadas():
                if texto in loc.nombre.lower():
                    coincidencias.append((mun, loc))

        return coincidencias

    def obtener_ranking_temperatura(self):
        """
        Calcula la localidad más cálida y la más fría registradas en la sesión.

        :return: Tupla (Localidad_mas_calida, Localidad_mas_fria) o (None, None).
        """
        mas_calida = self.estadisticas.obtener_mas_calida(self.consultas_sesion)
        mas_fria = self.estadisticas.obtener_mas_fria(self.consultas_sesion)
        return (mas_calida, mas_fria)

    def obtener_promedio_temperatura_sesion(self):
        """
        Calcula la temperatura promedio general de las consultas realizadas en la sesión.

        :return: Promedio en °C (float).
        """
        return self.estadisticas.calcular_promedio_temperatura(self.consultas_sesion)

    def obtener_cobertura_geografica_null(self):
        """
        Retorna la lista de localidades que NO poseen coordenadas (null), agrupadas por municipio.

        :return: Lista de tuplas (Municipio, lista_de_localidades_sin_coords).
        """
        reporte = []
        for mun in self.municipios:
            sin_coords = mun.localidades_sin_coordenadas()
            reporte.append((mun, sin_coords))
        return reporte
