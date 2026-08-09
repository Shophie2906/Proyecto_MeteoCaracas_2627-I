import json
import os
from models.Municipio import Municipio
from models.Localidad import Localidad

class JSONLoader:
    """Servicio encargado de la lectura y transformación de datos del archivo zonas_caracas.json en objetos del dominio."""

    @staticmethod
    def cargar_zonas(ruta_json="data/zonas_caracas.json"):
        """
        Carga el archivo JSON y construye las instancias de Municipio y Localidad.

        :param ruta_json: Ruta del archivo JSON a leer.
        :return: Lista de objetos Municipio cargados en memoria.
        """
        if not os.path.exists(ruta_json):
            # Intentar ruta alternativa relativa al archivo actual
            alt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "zonas_caracas.json"))
            if os.path.exists(alt_path):
                ruta_json = alt_path
            else:
                print(f"Error: No se encontró el archivo de datos en {ruta_json}")
                return []

        try:
            with open(ruta_json, "r", encoding="utf-8") as file:
                datos = json.load(file)
                municipios = []

                for item in datos.get("municipios", []):
                    nombre_mun = item.get("nombre")
                    m = Municipio(nombre=nombre_mun)

                    for loc in item.get("localidades", []):
                        nombre_loc = loc.get("nombre")
                        lat = loc.get("latitud")
                        lon = loc.get("longitud")

                        # Si latitud y longitud vienen como None o ausentes en el JSON,
                        # se instanciará la Localidad con latitud=None y longitud=None.
                        localidad_obj = Localidad(nombre=nombre_loc, latitud=lat, longitud=lon)
                        m.agregar_localidad(localidad_obj)

                    municipios.append(m)

                return municipios

        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"Error al leer/procesar el archivo JSON: {e}")
            return []
