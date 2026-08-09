class GeneradorReportes:
    """Módulo para dar formato imprimible a los datos."""

    @staticmethod
    def imprimir_clima_actual(municipio, clima):
        print("=" * 40)
        print(f" CLIMA ACTUAL EN: {municipio.nombre.upper()}")
        print("=" * 40)
        print(f" Temp. Registrada: {clima.temperatura} °C")
        print(f" Humedad Relativa: {clima.humedad} %")
        print(f" Precipitación:   {clima.precipitacion} mm")
        print(f" Viento:          {clima.velocidad_viento} km/h")
        print("=" * 40)
        