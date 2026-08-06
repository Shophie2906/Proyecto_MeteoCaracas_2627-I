from core.analizador import AnalizadorDatos

class Reportador:

    def mostrar_resumen(estacion):
        registros = estacion.obtener_registros()
        
        print("\n" + "="*45)
        print(f"   RESUMEN METEOROLÓGICO - {estacion.nombre.upper()}")
        print("="*45)
        
        if not registros:
            print("No hay registros almacenados todavía.")
            return

        print(f"Total de mediciones: {len(registros)}")
        print(f"• Temp. Promedio : {AnalizadorDatos.calcular_promedio_temperatura(registros)} °C")
        print(f"• Temp. Máxima   : {AnalizadorDatos.obtener_temperatura_maxima(registros)} °C")
        print(f"• Temp. Mínima   : {AnalizadorDatos.obtener_temperatura_minima(registros)} °C")
        print(f"• Lluvia Acumulada: {AnalizadorDatos.calcular_lluvia_total(registros)} mm")
        print("="*45)

    def listar_historial(estacion):
        registros = estacion.obtener_registros()
        print("\n--- HISTORIAL DE LECTURAS ---")
        if not registros:
            print("No hay lecturas registradas.")
            return
            
        for idx, reg in enumerate(registros, start=1):
            print(f"{idx}. {reg}")