from core.modelos import LecturaMeteorologica, Municipio
class ReportadorEstadisticas:
    """Clase encargada de procesar y visualizar los reportes estadísticos y métricas acumuladas durante la sesión activa del usuario."""

    @staticmethod
    def generar_reporte_sesion(
        historial: list[LecturaMeteorologica],
    ) -> None:
        """Calcula e imprime el ranking de temperaturas y el promedio general de las lecturas realizadas en la sesión activa.

        Args:
            historial (list[LecturaMeteorologica]): Lista de lecturas acumuladas"""
        print("\n" + "=" * 60)
        print("    ESTADÍSTICAS Y RANKING DE LA SESIÓN ACTIVA")
        print("=" * 60)

        if not historial:
            print(
                " Aún no se han realizado consultas meteorológicas en esta sesión."
            )
            print("=" * 60 + "\n")
            return

        # 1. Búsqueda de Máxima y Mínima Temperatura
        lectura_mas_calida = max(historial, key=lambda l: l.temperatura)
        lectura_mas_fria = min(historial, key=lambda l: l.temperatura)

        # 2. Promedio General de Temperatura
        suma_temperaturas = sum(l.temperatura for l in historial)
        promedio_general = suma_temperaturas / len(historial)

        print(f"Total de consultas realizadas en la sesión: {len(historial)}")
        print(f"Temperatura Promedio General:             {promedio_general:.2f} °C")
        print("-" * 60)
        print(" LOCALIDAD MÁS CÁLIDA:")
        print(
            f"   • Localidad:   {lectura_mas_calida.localidad_nombre} ({lectura_mas_calida.municipio_nombre})"
        )
        print(f"   • Temperatura: {lectura_mas_calida.temperatura} °C")
        print(f"   • Hora Lectura: {lectura_mas_calida.fecha_hora}")
        print("-" * 60)
        print(" LOCALIDAD MÁS FRÍA:")
        print(
            f"   • Localidad:   {lectura_mas_fria.localidad_nombre} ({lectura_mas_fria.municipio_nombre})"
        )
        print(f"   • Temperatura: {lectura_mas_fria.temperatura} °C")
        print(f"   • Hora Lectura: {lectura_mas_fria.fecha_hora}")
        print("=" * 60 + "\n")

    @staticmethod
    def reportar_localidades_sin_coordenadas(
        municipios: list[Municipio],
    ) -> None:
        """Muestra una lista detallada de todas las localidades que no poseen coordenadas geográficas registradas (null), agrupadas por municipio.

        Args:
            municipios (list[Municipio]): Lista completa de objetos Municipio"""
        print("\n" + "=" * 60)
        print("    LOCALIDADES SIN COORDENADAS REGISTRADAS (NULL)")
        print("=" * 60)

        total_sin_coords = 0

        for municipio in municipios:
            # Filtramos las localidades que no tienen coordenadas válidas
            sin_coords = [
                loc for loc in municipio.localidades if not loc.tiene_coordenadas()
            ]

            if sin_coords:
                print(f"\nMunicipio: {municipio.nombre}")
                for loc in sin_coords:
                    print(f"  {loc.nombre}")
                    total_sin_coords += 1

        if total_sin_coords == 0:
            print(" ¡Todas las localidades registradas poseen coordenadas válidas!")

        print("\n" + "=" * 60 + "\n")