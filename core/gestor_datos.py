import json
import os
from models.Municipio import Municipio
from models.Localidad import Localidad

class GestorDatos:
    """Manejo de lectura y escritura de archivos JSON locales."""

    @staticmethod
    def cargar_zonas(ruta_json="zonas_caracas.json"):
        """Carga las ubicaciones (municipios y localidades) desde un JSON."""
        if not os.path.exists(ruta_json):
            print(f"El archivo {ruta_json} no existe.")
            return []

        try:
            with open(ruta_json, "r", encoding="utf-8") as file:
                datos = json.load(file)
                municipios = []
                
                for item in datos.get("municipios", []):
                    m = Municipio(
                        nombre=item.get("nombre"),
                        latitud=item.get("latitud"),
                        longitud=item.get("longitud")
                    )
                    # Cargar localidades asociadas
                    for loc in item.get("localidades", []):
                        m.agregar_localidad(Localidad(nombre=loc.get("nombre")))
                    
                    municipios.append(m)
                return municipios

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al procesar el archivo JSON: {e}")
            return []

    @staticmethod
    def guardar_json(datos, ruta_archivo):
        """Guarda cualquier estructura de datos en formato JSON."""
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as file:
                json.dump(datos, file, ensure_ascii=False, indent=4)
            print(f"Datos guardados exitosamente en {ruta_archivo}")
        except IOError as e:
            print(f"Error al escribir en {ruta_archivo}: {e}")