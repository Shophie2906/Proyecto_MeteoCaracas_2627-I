import requests
import matplotlib.pyplot as plt
from datetime import datetime

class HistoricoManager:
    """Módulo para consultar datos históricos en Open-Meteo y generar gráficos comparativos."""

    URL_HISTORICO = "https://archive-api.open-meteo.com/v1/archive"

    @staticmethod
    def consultar_historico(localidad, fecha_inicio, fecha_fin):
        """
        Consulta el rango de fechas histórico para una localidad y genera estadísticas/gráficos.
        
        :param localidad: Objeto de la clase Localidad.
        :param fecha_inicio: Cadena con formato YYYY-MM-DD.
        :param fecha_fin: Cadena con formato YYYY-MM-DD.
        """
        if not localidad.tiene_coordenadas():
            print(f" La localidad '{localidad.nombre}' no tiene coordenadas para consulta histórica.")
            return

        params = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": ["temperature_2m_mean", "relative_humidity_2m_mean", "precipitation_sum", "wind_speed_10m_max"],
            "timezone": "America/Caracas"
        }

        try:
            print(f" Consultando historial en Open-Meteo para '{localidad.nombre}'...")
            respuesta = requests.get(HistoricoManager.URL_HISTORICO, params=params, timeout=10)

            if respuesta.status_code == 200:
                data = respuesta.json().get("daily", {})
                fechas = data.get("time", [])
                temperaturas = data.get("temperature_2m_mean", [])
                humedades = data.get("relative_humidity_2m_mean", [])
                precipitaciones = data.get("precipitation_sum", [])
                vientos = data.get("wind_speed_10m_max", [])

                if not fechas:
                    print(" No se encontraron registros para el rango de fechas especificado.")
                    return

                # Procesamiento por años
                datos_por_anio = {}
                for i, fecha_str in enumerate(fechas):
                    anio = fecha_str.split("-")[0]
                    if anio not in datos_por_anio:
                        datos_por_anio[anio] = {
                            "temp": [], "hum": [], "prec": [], "viento": []
                        }
                    
                    if temperaturas[i] is not None: datos_por_anio[anio]["temp"].append(temperaturas[i])
                    if humedades[i] is not None: datos_por_anio[anio]["hum"].append(humedades[i])
                    if precipitaciones[i] is not None: datos_por_anio[anio]["prec"].append(precipitaciones[i])
                    if vientos[i] is not None: datos_por_anio[anio]["viento"].append(vientos[i])

                # Promedios y Récords Anuales
                resumen_anios = {}
                print("\n" + "="*60)
                print(f" RESUMEN HISTÓRICO: {localidad.nombre.upper()}")
                print("="*60)

                for anio, vals in datos_por_anio.items():
                    avg_t = sum(vals["temp"]) / len(vals["temp"]) if vals["temp"] else 0
                    avg_h = sum(vals["hum"]) / len(vals["hum"]) if vals["hum"] else 0
                    sum_p = sum(vals["prec"]) if vals["prec"] else 0
                    avg_v = sum(vals["viento"]) / len(vals["viento"]) if vals["viento"] else 0

                    resumen_anios[anio] = {
                        "avg_temp": avg_t, "avg_hum": avg_h,
                        "sum_prec": sum_p, "avg_viento": avg_v
                    }

                    print(f"\n📅 AÑO {anio}:")
                    print(f" • Temp. Promedio  : {avg_t:.2f} °C")
                    print(f" • Humedad Promedio: {avg_h:.2f} %")
                    print(f" • Lluvia Acumulada: {sum_p:.2f} mm")
                    print(f" • Viento Promedio : {avg_v:.2f} km/h")

                # Identificar Extremos (Año más caluroso, fresco, lluvioso, húmedo)
                anio_mas_calido = max(resumen_anios.items(), key=lambda x: x[1]["avg_temp"])[0]
                anio_mas_fresco = min(resumen_anios.items(), key=lambda x: x[1]["avg_temp"])[0]
                anio_mas_lluvioso = max(resumen_anios.items(), key=lambda x: x[1]["sum_prec"])[0]
                anio_mas_humedo = max(resumen_anios.items(), key=lambda x: x[1]["avg_hum"])[0]

                print("\n" + "-"*60)
                print(" REGISTROS EXTREMOS EN EL PERÍODO:")
                print(f"  Año más caluroso : {anio_mas_calido} ({resumen_anios[anio_mas_calido]['avg_temp']:.2f} °C)")
                print(f"  Año más fresco   : {anio_mas_fresco} ({resumen_anios[anio_mas_fresco]['avg_temp']:.2f} °C)")
                print(f"  Año más lluvioso : {anio_mas_lluvioso} ({resumen_anios[anio_mas_lluvioso]['sum_prec']:.2f} mm)")
                print(f"  Año más húmedo   : {anio_mas_humedo} ({resumen_anios[anio_mas_humedo]['avg_hum']:.2f} %)")
                print("="*60)

                # Generar Gráfico Comparativo Matplotlib
                HistoricoManager.generar_grafico(localidad.nombre, resumen_anios)

            else:
                print(f" Error al consultar histórico (Código HTTP: {respuesta.status_code}).")

        except Exception as e:
            print(f" Error al procesar histórico: {e}")

    @staticmethod
    def generar_grafico(nombre_localidad, resumen_anios):
        """
        Genera un gráfico comparativo de evolución de magnitudes meteorológicas.
        
        :param nombre_localidad: Nombre de la localidad.
        :param resumen_anios: Diccionario con estadísticas agregadas por año.
        """
        anios = list(resumen_anios.keys())
        temps = [resumen_anios[a]["avg_temp"] for a in anios]
        hums = [resumen_anios[a]["avg_hum"] for a in anios]
        precs = [resumen_anios[a]["sum_prec"] for a in anios]

        plt.figure(figsize=(10, 6))

        plt.subplot(2, 1, 1)
        plt.plot(anios, temps, marker='o', color='tab:red', label='Temp Promedio (°C)')
        plt.plot(anios, hums, marker='s', color='tab:blue', label='Humedad Promedio (%)')
        plt.title(f'Evolución Meteorológica Histórica - {nombre_localidad}')
        plt.ylabel('Magnitud')
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.bar(anios, precs, color='tab:green', alpha=0.7, label='Precipitación Acumulada (mm)')
        plt.xlabel('Año')
        plt.ylabel('Precipitación (mm)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        print("\n Generando gráfico comparativo... Cierra la ventana del gráfico para continuar.")
        plt.show()