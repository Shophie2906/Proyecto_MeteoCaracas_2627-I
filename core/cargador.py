import json
from core import Municipio, Localidad

class CargadorDatos:
    """Clase encargada de leer el archivo zonas_caracas.json y transformar su estructura en objetos de dominio (Municipio y Localidad)."""

    @staticmethod
    def cargar_municipios(ruta_json: str) -> list[Municipio]:
        """Lee el JSON y devuelve una lista de objetos Municipio."""
        lista_municipios: list[Municipio] = []
        try:
            with open(ruta_json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                for nombre_mun, localidades_dict in datos.items():
                    municipio_obj = Municipio(nombre_mun)
                    for loc_nombre, coords in localidades_dict.items():
                        lat = coords.get("lat") if coords else None
                        lon = coords.get("lon") if coords else None
                        localidad_obj = Localidad(nombre=loc_nombre, latitud=lat, longitud=lon)
                        municipio_obj.agregar_localidad(localidad_obj)
                    lista_municipios.append(municipio_obj)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{ruta_json}'.")
        return lista_municipios

    @staticmethod
    def generar_reporte_cobertura(municipios: list[Municipio]) -> None:
        """Imprime el reporte inicial de localidades con/sin coordenadas."""
        print("\n" + "=" * 60)
        print("    REPORTE DE COBERTURA GEOGRÁFICA DE LOCALIDADES")
        print("=" * 60)
        for municipio in municipios:
            stats = municipio.obtener_cobertura()
            print(f"\nMunicipio: {municipio.nombre}")
            print(f"  • Total de localidades cargadas: {stats['total']}")
            print(f"  • Con coordenadas geográficas:   {stats['con_coords']}")
            print(f"  • Sin coordenadas geográficas:   {stats['sin_coords']}")
            print(f"  • Cobertura geográfica:          {stats['porcentaje']:.2f}%")
        print("=" * 60 + "\n")