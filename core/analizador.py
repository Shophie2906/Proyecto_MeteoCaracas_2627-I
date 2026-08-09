import matplotlib.pyplot as plt
from core.api_client import APIClient
from core.modelos import LecturaMeteorologica, Localidad, Municipio
class AnalizadorDatos:
    """Clase encargada de procesar métricas en tiempo real, estadísticas de la sesión activa y la generación de gráficos e informes históricos."""

    # --- 1. ESTADÍSTICAS DE LA SESIÓN ACTIVA ---
    @staticmethod
    def generar_reporte_sesion(
        historial: list[LecturaMeteorologica],
    ) -> None:
        """Calcula el ranking de temperaturas (máx/mín) y el promedio general de las consultas hechas en la sesión."""
        print("\n" + "=" * 60)
        print("    ESTADÍSTICAS Y RANKING DE LA SESIÓN ACTIVA")
        print("=" * 60)

        if not historial:
            print(
                " Aún no se han realizado consultas meteorológicas en esta sesión."
            )
            print("=" * 60 + "\n")
            return

        lectura_mas_calida = max(historial, key=lambda l: l.temperatura)
        lectura_mas_fria = min(historial, key=lambda l: l.temperatura)
        promedio_general = sum(l.temperatura for l in historial) / len(
            historial
        )

        print(f"Total de consultas realizadas:           {len(historial)}")
        print(
            f"Temperatura Promedio General:             {promedio_general:.2f} °C"
        )
        print("-" * 60)
        print(
            f" MÁS CÁLIDA: {lectura_mas_calida.localidad_nombre} ({lectura_mas_calida.municipio_nombre}) -> {lectura_mas_calida.temperatura} °C"
        )
        print(
            f" MÁS FRÍA:   {lectura_mas_fria.localidad_nombre} ({lectura_mas_fria.municipio_nombre}) -> {lectura_mas_fria.temperatura} °C"
        )
        print("=" * 60 + "\n")

    # --- 2. ANÁLISIS HISTÓRICO Y GRÁFICOS ---
    @classmethod
    def analizar_y_graficar_historico(
        cls, localidad: Localidad, fecha_inicio: str, fecha_fin: str
    ) -> None:
        """Consulta el histórico de Open-Meteo para una localidad y muestra

        las estadísticas junto al gráfico de Matplotlib.
        """
        print(
            f"\n Consultando datos históricos para '{localidad.nombre}' ({fecha_inicio} a {fecha_fin})..."
        )

        datos_json = APIClient.obtener_historial_diario(
            localidad, fecha_inicio, fecha_fin
        )

        if not datos_json or "daily" not in datos_json:
            print(
                " No se pudieron obtener datos históricos para el rango especificado."
            )
            return

        diario = datos_json["daily"]
        fechas = diario.get("time", [])
        temp_max = diario.get("temperature_2m_max", [])
        temp_min = diario.get("temperature_2m_min", [])
        temp_med = diario.get("temperature_2m_mean", [])
        precipitacion = diario.get("precipitation_sum", [])
        humedad = diario.get("relative_humidity_2m_mean", [])

        if not fechas:
            print(" No hay registros para mostrar en el rango seleccionado.")
            return

        # Métricas
        temp_promedio = sum(temp_med) / len(temp_med) if temp_med else 0.0
        precip_total = sum(p for p in precipitacion if p is not None)
        humedad_promedio = (
            sum(h for h in humedad if h is not None) / len(humedad)
            if humedad
            else 0.0
        )

        max_temp_val = max(temp_max)
        fecha_mas_calida = fechas[temp_max.index(max_temp_val)]

        min_temp_val = min(temp_min)
        fecha_mas_fria = fechas[temp_min.index(min_temp_val)]

        print("\n" + "=" * 60)
        print(f"    RESUMEN HISTÓRICO: {localidad.nombre.upper()}")
        print("=" * 60)
        print(
            f"• Período evaluado:         {fecha_inicio} a {fecha_fin} ({len(fechas)} días)"
        )
        print(f"• Temperatura Promedio:     {temp_promedio:.2f} °C")
        print(
            f"• Día más caluroso:         {fecha_mas_calida} ({max_temp_val} °C)"
        )
        print(f"• Día más fresco:           {fecha_mas_fria} ({min_temp_val} °C)")
        print(f"• Precipitación Acumulada:   {precip_total:.2f} mm")
        print(f"• Humedad Promedio:         {humedad_promedio:.2f} %")
        print("=" * 60 + "\n")

        # Visualización
        cls._generar_grafico(
            localidad.nombre, fechas, temp_max, temp_min, precipitacion
        )

    @staticmethod
    def _generar_grafico(
        nombre_localidad: str,
        fechas: list,
        temp_max: list,
        temp_min: list,
        precipitacion: list,
    ) -> None:
        """Renderiza la gráfica combinada de Temperatura y Precipitación."""
        fig, ax1 = plt.subplots(figsize=(10, 5))

        ax1.set_xlabel("Fecha", fontweight="bold")
        ax1.set_ylabel("Temperatura (°C)", color="tab:red", fontweight="bold")
        ax1.plot(
            fechas,
            temp_max,
            color="crimson",
            marker="o",
            linewidth=2,
            label="Temp Max",
        )
        ax1.plot(
            fechas,
            temp_min,
            color="royalblue",
            marker="o",
            linewidth=2,
            label="Temp Min",
        )
        ax1.tick_params(axis="y", labelcolor="tab:red")
        plt.xticks(rotation=45, ha="right")

        ax2 = ax1.twinx()
        ax2.set_ylabel(
            "Precipitación (mm)", color="tab:blue", fontweight="bold"
        )
        ax2.bar(
            fechas,
            precipitacion,
            color="skyblue",
            alpha=0.4,
            label="Precipitación",
        )
        ax2.tick_params(axis="y", labelcolor="tab:blue")

        plt.title(
            f"Evolución Meteorológica - {nombre_localidad}",
            fontsize=13,
            fontweight="bold",
        )
        fig.tight_layout()
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.show()