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

            # Diccionario auxiliar para agrupar localidades por municipio
            municipios_dict = {}

            for item in datos:
                nombre_mun = item.get("municipio")
                if not nombre_mun:
                    continue

                # Si el municipio no ha sido creado, lo instanciamos
                if nombre_mun not in municipios_dict:
                    municipios_dict[nombre_mun] = Municipio(nombre=nombre_mun)

                # Creamos la localidad y se la agregamos al municipio
                # (Ajusta los nombres de las claves según las propiedades de tu clase Localidad)
                loc = Localidad(
                    nombre=item.get("nombre") or item.get("localidad"),
                    latitud=item.get("latitud"),
                    longitud=item.get("longitud"),
                )

                # Si tu clase Municipio tiene un método agregar_localidad o atributo localidades:
                if hasattr(municipios_dict[nombre_mun], "agregar_localidad"):
                    municipios_dict[nombre_mun].agregar_localidad(loc)
                elif hasattr(municipios_dict[nombre_mun], "localidades"):
                    municipios_dict[nombre_mun].localidades.append(loc)

            return list(municipios_dict.values())

        except Exception as e:
            print(f"Error al leer/procesar el archivo JSON: {e}")
            return []
        
