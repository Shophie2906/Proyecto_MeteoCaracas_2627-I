from core.gestor_datos import GestorDatos
from core.api_client import APIClient
from core.historico_manager import HistoricoManager

def mostrar_menu():
    print("\n" + "="*50)
    print( " SISTEMA METEOROLÓGICO METEOCARACAS")
    print("="*50)
    print(" 1. Ver municipios y reporte inicial")
    print(" 2. Consultar clima: Selección por Municipio")
    print(" 3. Consultar clima: Búsqueda directa por nombre")
    print(" 4. Reportes y Estadísticas de la sesión")
    print(" 5. Consulta de Históricos y Gráficos Comparativos")
    print(" 6. Salir")
    print("="*50)

def main():
    municipios = GestorDatos.cargar_datos("zonas_caracas.json")

    if not municipios:
        print(" No se pudieron cargar los municipios. Revisa el archivo JSON.")
        return

    consultas_sesion = []

    while True:
        mostrar_menu()
        opcion = input("\n Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            GestorDatos.imprimir_reporte_inicial_desglosado(municipios)

        elif opcion == "2":
            print("\n MUNICIPIOS DISPONIBLES:")
            for i, mun in enumerate(municipios, 1):
                print(f" {i}. {mun.nombre}")

            idx_m = input("\nSelecciona el número del municipio: ").strip()
            if idx_m.isdigit() and 1 <= int(idx_m) <= len(municipios):
                mun_sel = municipios[int(idx_m) - 1]
                locs_validas = mun_sel.obtener_localidades_con_coords()

                if not locs_validas:
                    print(f" El municipio {mun_sel.nombre} no tiene localidades con coordenadas válidas.")
                else:
                    print(f"\n LOCALIDADES CON COORDENADAS EN {mun_sel.nombre.upper()}:")
                    for j, loc in enumerate(locs_validas, 1):
                        print(f" {j}. {loc.nombre}")

                    idx_l = input("\nSelecciona la localidad a consultar: ").strip()
                    if idx_l.isdigit() and 1 <= int(idx_l) <= len(locs_validas):
                        loc_sel = locs_validas[int(idx_l) - 1]
                        reporte = APIClient.obtener_clima_localidad(loc_sel)
                        if reporte:
                            consultas_sesion.append((mun_sel, loc_sel, reporte))
                            print(f"\n REPORTE EN TIEMPO REAL:")
                            print(f" • Municipio/Localidad: {mun_sel.nombre} - {loc_sel.nombre}")
                            print(f" • Coordenadas       : ({loc_sel.latitud}, {loc_sel.longitud})")
                            print(f" • Detalle           : {reporte}")
                    else:
                        print(" Selección de localidad inválida.")
            else:
                print(" Selección de municipio inválida.")

        elif opcion == "3":
            texto = input("\n Ingresa el nombre (o parte) de la localidad: ").strip()
            coincidencias = []

            for mun in municipios:
                encontradas = mun.buscar_localidad_parcial(texto)
                for loc in encontradas:
                    coincidencias.append((mun, loc))

            if not coincidencias:
                print(f" No se encontraron coincidencias para '{texto}'.")
            else:
                print(f"\n🔎 RESULTADOS ENCONTRADOS ({len(coincidencias)}):")
                for k, (m, l) in enumerate(coincidencias, 1):
                    estado = f"({l.latitud}, {l.longitud})" if l.tiene_coordenadas() else "[Sin Coordenadas]"
                    print(f" {k}. {l.nombre} ({m.nombre}) - {estado}")

                idx_c = input("\nSelecciona el número de la localidad deseada: ").strip()
                if idx_c.isdigit() and 1 <= int(idx_c) <= len(coincidencias):
                    m_sel, l_sel = coincidencias[int(idx_c) - 1]
                    if not l_sel.tiene_coordenadas():
                        print(f" La localidad '{l_sel.nombre}' no posee coordenadas válidas.")
                    else:
                        reporte = APIClient.obtener_clima_localidad(l_sel)
                        if reporte:
                            consultas_sesion.append((m_sel, l_sel, reporte))
                            print(f"\n REPORTE EN TIEMPO REAL:")
                            print(f" • Municipio/Localidad: {m_sel.nombre} - {l_sel.nombre}")
                            print(f" • Coordenadas       : ({l_sel.latitud}, {l_sel.longitud})")
                            print(f" • Detalle           : {reporte}")
                else:
                    print(" Selección inválida.")

        elif opcion == "4":
            print("\n" + "="*50)
            print(" REPORTES Y ESTADÍSTICAS DE LA SESIÓN")
            print("="*50)

            print("\n LOCALIDADES SIN COORDENADAS REGISTRADAS (NULL):")
            for mun in municipios:
                sin_coords = mun.obtener_localidades_sin_coords()
                if sin_coords:
                    print(f" • {mun.nombre}:")
                    for loc in sin_coords:
                        print(f"    └─ {loc.nombre}")

            if not consultas_sesion:
                print("\n Aún no has realizado ninguna consulta de clima en esta sesión.")
            else:
                mas_calida = max(consultas_sesion, key=lambda x: x[2].temperatura)
                mas_fria = min(consultas_sesion, key=lambda x: x[2].temperatura)
                promedio_temp = sum(item[2].temperatura for item in consultas_sesion) / len(consultas_sesion)

                print("\n LOCALIDAD MÁS CÁLIDA CONSULTADA:")
                print(f"   └─ {mas_calida[0].nombre} ({mas_calida[1].nombre}): {mas_calida[2].temperatura}°C")

                print("\n LOCALIDAD MÁS FRÍA CONSULTADA:")
                print(f"   └─ {mas_fria[0].nombre} ({mas_fria[1].nombre}): {mas_fria[2].temperatura}°C")

                print(f"\n PROMEDIO GENERAL DE TEMPERATURA: {promedio_temp:.2f}°C")

        elif opcion == "5":
            # Requerimiento 4: Históricos y Gráficos
            texto = input("\n Ingresa la localidad para consultar histórico: ").strip()
            loc_encontrada = None

            for mun in municipios:
                res = mun.buscar_localidad_parcial(texto)
                if res:
                    loc_encontrada = res[0]
                    break

            if not loc_encontrada:
                print(f" No se encontró la localidad '{texto}'.")
            elif not loc_encontrada.tiene_coordenadas():
                print(f" La localidad '{loc_encontrada.nombre}' no tiene coordenadas válidas.")
            else:
                f_inicio = input("Ingresa fecha de inicio (AAAA-MM-DD, ej. 2022-01-01): ").strip()
                f_fin = input("Ingresa fecha de fin (AAAA-MM-DD, ej. 2024-12-31): ").strip()
                
                HistoricoManager.consultar_historico(loc_encontrada, f_inicio, f_fin)

        elif opcion == "6":
            print("\n¡Gracias por utilizar MeteoCaracas! \n")
            break
        else:
            print(" Opción no válida. Ingresa un número del 1 al 6.")

if __name__ == "__main__":
    main()