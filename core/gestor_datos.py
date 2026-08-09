import json
from models.modelos import Municipio, Localidad

class GestorDatos:
    """Módulo encargado de leer el JSON territorial y generar reportes iniciales de carga."""

    @staticmethod
    def cargar_datos(ruta_json="zonas_caracas.json"):
        """
        Lee el archivo JSON de localidades y construye objetos Municipio y Localidad.
        
        :param ruta_json: Ruta del archivo JSON a procesar.
        :return: Lista de objetos Municipio.
        """
        municipios_dict = {}

        try:
            with open(ruta_json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            for item in datos:
                nombre_mun = item.get("municipio", "Desconocido")
                nombre_loc = item.get("localidad", "Sin Nombre")
                lat = item.get("latitud")
                lng = item.get("longitud")

                if nombre_mun not in municipios_dict:
                    municipios_dict[nombre_mun] = Municipio(nombre_mun)

                nueva_loc = Localidad(nombre_loc, lat, lng)
                municipios_dict[nombre_mun].agregar_localidad(nueva_loc)

            lista_municipios = list(municipios_dict.values())
            
            GestorDatos.imprimir_reporte_inicial_desglosado(lista_municipios)
            
            return lista_municipios

        except FileNotFoundError:
            print(f" Error: No se encontró el archivo '{ruta_json}'.")
            return []
        except json.JSONDecodeError:
            print(f" Error: El archivo '{ruta_json}' no es un JSON válido.")
            return []

    @staticmethod
    def imprimir_reporte_inicial_desglosado(municipios):
        """
        Genera en pantalla el reporte estadístico de carga por cada municipio.
        
        :param municipios: Lista de objetos Municipio.
        """
        print("\n" + "="*65)
        print(" REPORTE DE CARGA INICIAL POR MUNICIPIO (METEOCARACAS)")
        print("="*65)

        total_general = 0
        total_con_coords_gen = 0

        for mun in municipios:
            total_loc = len(mun.localidades)
            con_coords = len(mun.obtener_localidades_con_coords())
            sin_coords = len(mun.obtener_localidades_sin_coords())
            pct_con = (con_coords / total_loc * 100) if total_loc > 0 else 0.0

            total_general += total_loc
            total_con_coords_gen += con_coords

            print(f" MUNICIPIO: {mun.nombre}")
            print(f"   a. Localidades cargadas         : {total_loc}")
            print(f"   b. Con coordenadas geográficas  : {con_coords}")
            print(f"   c. Sin coordenadas conocidas    : {sin_coords}")
            print(f"   d. Cobertura con coordenadas    : {pct_con:.1f}%")
            print("-" * 65)

        pct_general = (total_con_coords_gen / total_general * 100) if total_general > 0 else 0.0
        print(f"TOTAL GENERAL: {total_general} localidades | Cobertura global: {pct_general:.1f}%")
        print("="*65 + "\n")