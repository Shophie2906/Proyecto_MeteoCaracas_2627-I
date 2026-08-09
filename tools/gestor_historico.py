import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from models.RegistroHistorico import RegistroHistorico
from db.open_meteo_service import OpenMeteoService

class GestorHistorico:
    """Controlador responsable del análisis histórico de datos meteorológicos y generación de gráficos."""

    MESES_ESPANOL = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    def __init__(self):
        pass

    def consultar_historico(self, localidad, fecha_inicio, fecha_fin):
        """
        Obtiene los datos meteorológicos históricos de una localidad entre dos fechas,
        los procesa mes a mes y devuelve una lista de objetos RegistroHistorico.

        :param localidad: Instancia de Localidad con coordenadas.
        :param fecha_inicio: Fecha de inicio en formato AAAA-MM-DD.
        :param fecha_fin: Fecha de fin en formato AAAA-MM-DD.
        :return: Tupla (lista_objetos_RegistroHistorico, resumen_promedios, resumen_extremos_anuales) o (None, None, None).
        """
        if not localidad.tiene_coordenadas():
            print(f"Error: La localidad '{localidad.nombre}' no posee coordenadas válidas.")
            return None, None, None

        datos_raw = OpenMeteoService.obtener_datos_historicos(
            localidad.latitud, localidad.longitud, fecha_inicio, fecha_fin
        )

        if not datos_raw or "time" not in datos_raw or len(datos_raw["time"]) == 0:
            print("Error: No se obtuvieron datos históricos para el período especificado.")
            return None, None, None

        # Convertimos la información horaria de la API a un DataFrame de Pandas
        df = pd.DataFrame(datos_raw)
        df['time'] = pd.to_datetime(df['time'])
        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['month_name'] = df['month'].map(self.MESES_ESPANOL)

        # Aseguramos columnas numéricas limpias para evitar errores de tipo
        for col in ['temperature_2m', 'relative_humidity_2m', 'precipitation', 'wind_speed_10m']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            else:
                df[col] = 0.0

        # Agrupamos mensualmente (Año, Mes) ordenados cronológicamente
        agrupado_mes = df.groupby(['year', 'month', 'month_name'], sort=False).agg(
            temp_prom=('temperature_2m', 'mean'),
            hum_prom=('relative_humidity_2m', 'mean'),
            prec_sum=('precipitation', 'sum'),
            viento_prom=('wind_speed_10m', 'mean')
        ).reset_index()

        registros_mensuales = []
        for _, row in agrupado_mes.iterrows():
            registro = RegistroHistorico(
                mes=str(row['month_name']),
                anio=int(row['year']),
                temperatura=round(float(row['temp_prom']), 2),
                humedad=round(float(row['hum_prom']), 2),
                precipitacion=round(float(row['prec_sum']), 2),
                velocidad_viento=round(float(row['viento_prom']), 2)
            )
            registros_mensuales.append(registro)

        # Cálculo de valores promedios del período completo (Requerimiento 4.b)
        promedios = {
            'temperatura': round(float(df['temperature_2m'].mean()), 2),
            'humedad': round(float(df['relative_humidity_2m'].mean()), 2),
            'precipitacion': round(float(agrupado_mes['prec_sum'].mean()), 2),
            'velocidad_viento': round(float(df['wind_speed_10m'].mean()), 2)
        }

        # Cálculo del resumen por año (Requerimiento 4.c)
        agrupado_anio = df.groupby('year').agg(
            temp_prom=('temperature_2m', 'mean'),
            hum_prom=('relative_humidity_2m', 'mean'),
            prec_total=('precipitation', 'sum')
        ).reset_index()

        if not agrupado_anio.empty:
            anio_mas_caluroso = int(agrupado_anio.loc[agrupado_anio['temp_prom'].idxmax()]['year'])
            anio_mas_fresco = int(agrupado_anio.loc[agrupado_anio['temp_prom'].idxmin()]['year'])
            anio_mas_precipitacion = int(agrupado_anio.loc[agrupado_anio['prec_total'].idxmax()]['year'])
            anio_mas_humedad = int(agrupado_anio.loc[agrupado_anio['hum_prom'].idxmax()]['year'])
        else:
            anio_mas_caluroso = anio_mas_fresco = anio_mas_precipitacion = anio_mas_humedad = "N/A"

        extremos = {
            'caluroso': anio_mas_caluroso,
            'fresco': anio_mas_fresco,
            'precipitacion': anio_mas_precipitacion,
            'humedad': anio_mas_humedad
        }

        return registros_mensuales, promedios, extremos

    def generar_grafico_historico(self, registros_mensuales, nombre_localidad):
        """
        Genera y despliega un gráfico de 4 subplots comparando la evolución mensual de las 4 magnitudes
        principales por cada año dentro del período especificado (Requerimiento 4.d).

        :param registros_mensuales: Lista de objetos RegistroHistorico.
        :param nombre_localidad: Nombre de la localidad consultada (str).
        """
        if not registros_mensuales:
            print("No existen registros suficientes para generar el gráfico.")
            return

        # Obtenemos los años únicos para la comparación año a año
        anios = sorted(list(set(r.anio for r in registros_mensuales)))

        fig, axs = plt.subplots(2, 2, figsize=(14, 8))
        fig.suptitle(f"Evolución Meteorológica Comparativa - {nombre_localidad}", fontsize=16, fontweight='bold')

        # Paleta de colores para los distintos años
        colores = plt.cm.tab10(np.linspace(0, 1, max(len(anios), 1)))

        for i, anio in enumerate(anios):
            regs_anio = [r for r in registros_mensuales if r.anio == anio]

            x_labels = [r.obtener_nombre_mes()[:3] for r in regs_anio]
            temps = [r.temperatura for r in regs_anio]
            hums = [r.humedad for r in regs_anio]
            precs = [r.precipitacion for r in regs_anio]
            vientos = [r.velocidad_viento for r in regs_anio]

            color = colores[i]
            label = f"Año {anio}"

            # Subplot 1: Temperatura
            axs[0, 0].plot(x_labels, temps, marker='o', label=label, color=color, linewidth=2)
            # Subplot 2: Humedad Relativa
            axs[0, 1].plot(x_labels, hums, marker='s', label=label, color=color, linewidth=2)
            # Subplot 3: Precipitación Acumulada
            axs[1, 0].plot(x_labels, precs, marker='d', label=label, color=color, linewidth=2)
            # Subplot 4: Velocidad del Viento
            axs[1, 1].plot(x_labels, vientos, marker='^', label=label, color=color, linewidth=2)

        # Configuración de Subplot 1: Temperatura
        axs[0, 0].set_title("Temperatura Promedio Mensual (°C)")
        axs[0, 0].set_ylabel("°C")
        axs[0, 0].grid(True, linestyle='--', alpha=0.5)
        axs[0, 0].legend(title="Período")

        # Configuración de Subplot 2: Humedad Relativa
        axs[0, 1].set_title("Humedad Relativa Promedio (%)")
        axs[0, 1].set_ylabel("%")
        axs[0, 1].grid(True, linestyle='--', alpha=0.5)
        axs[0, 1].legend(title="Período")

        # Configuración de Subplot 3: Precipitación Acumulada
        axs[1, 0].set_title("Precipitación Acumulada Mensual (mm)")
        axs[1, 0].set_ylabel("mm")
        axs[1, 0].grid(True, linestyle='--', alpha=0.5)
        axs[1, 0].legend(title="Período")

        # Configuración de Subplot 4: Velocidad del Viento
        axs[1, 1].set_title("Velocidad Promedio del Viento (km/h)")
        axs[1, 1].set_ylabel("km/h")
        axs[1, 1].grid(True, linestyle='--', alpha=0.5)
        axs[1, 1].legend(title="Período")

        plt.tight_layout()
        plt.show()
