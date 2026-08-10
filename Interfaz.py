from datetime import datetime

class Interfaz:
    """Gestiona el menú interactivo de consola, navegación y validaciones de entrada del usuario."""

    def __init__(self, gestor_clima, gestor_historico):
        """
        Inicializa la interfaz de consola conectándola a los controladores del sistema.

        :param gestor_clima: Instancia del controlador GestorClima.
        :param gestor_historico: Instancia del controlador GestorHistorico.
        """
        self.gestor_clima = gestor_clima
        self.gestor_historico = gestor_historico

    def validar_entera(self, mensaje, minimo, maximo):
        """
        Solicita un número entero por teclado dentro de un rango inclusivo [minimo, maximo].

        :param mensaje: Texto que solicita la entrada.
        :param minimo: Valor mínimo permitido.
        :param maximo: Valor máximo permitido.
        :return: Número entero validado.
        """
        while True:
            try:
                opcion = int(input(mensaje))
                if minimo <= opcion <= maximo:
                    return opcion
                print(f"   [!] Error: Ingrese un numero entre {minimo} y {maximo}.")
            except ValueError:
                print("   [!] Error: Por favor ingrese un numero entero valido.")

    def validar_fecha(self, mensaje):
        """
        Solicita y valida una fecha en formato AAAA-MM-DD.

        :param mensaje: Prompt a mostrar al usuario.
        :return: Cadena de texto validada en formato AAAA-MM-DD.
        """
        while True:
            entrada = input(mensaje).strip()
            try:
                fecha_obj = datetime.strptime(entrada, "%Y-%m-%d")
                return fecha_obj.strftime("%Y-%m-%d")
            except ValueError:
                print("   [!] Error: Formato invalido. Debe ingresar la fecha en formato AAAA-MM-DD (ej. 2023-01-01).")

    def Start(self):
        """Ejecuta el ciclo principal del menú interactivo de la aplicación."""
        while True:
            print("\n" + "=" * 55)
            print(" SISTEMA DE MONITOREO METEOROLOGICO METEOCARACAS ")
            print("=" * 55)
            print(" 1. Reporte inicial de carga de localidades")
            print(" 2. Consulta del clima en tiempo real")
            print(" 3. Reportes y estadisticas de sesion")
            print(" 4. Analisis historico y graficos")
            print(" 5. Salir del programa")
            print("=" * 55)

            opcion = self.validar_entera(" Indique su eleccion (1-5): ", 1, 5)

            if opcion == 1:
                self.mostrar_reporte_carga_inicial()
            elif opcion == 2:
                self.menu_consulta_tiempo_real()
            elif opcion == 3:
                self.menu_estadisticas_sesion()
            elif opcion == 4:
                self.menu_historico()
            elif opcion == 5:
                print("\n ¡Gracias por utilizar MeteoCaracas! Hasta luego.\n")
                break

    def mostrar_reporte_carga_inicial(self):
        """Muestra el reporte detallado de cobertura territorial por municipio tras la carga (Requerimiento 1)."""
        print("\n" + "=" * 60)
        print(" REPORTE DE COBERTURA DE CARGA INICIAL DE LOCALIDADES")
        print("=" * 60)

        for mun in self.gestor_clima.municipios:
            total = mun.total_localidades()
            con_coords = len(mun.localidades_con_coordenadas())
            sin_coords = len(mun.localidades_sin_coordenadas())
            pct = mun.porcentaje_con_coordenadas()

            print(f"\n [-] Municipio: {mun.nombre}")
            print(f"    |- Total localidades cargadas: {total}")
            print(f"    |- Con coordenadas geograficas: {con_coords}")
            print(f"    |- Sin coordenadas conocidas (null): {sin_coords}")
            print(f"    |- Porcentaje de cobertura: {pct}%")

    def menu_consulta_tiempo_real(self):
        """Maneja el submenu para la consulta de clima en tiempo real (Requerimiento 2)."""
        while True:
            print("\n --- CONSULTA DEL CLIMA EN TIEMPO REAL ---")
            print(" 1. Consulta por municipio y localidad")
            print(" 2. Busqueda directa por nombre de localidad")
            print(" 3. Volver al menu principal")

            opcion = self.validar_entera(" Seleccione una modalidad (1-3): ", 1, 3)

            if opcion == 1:
                self._consultar_por_municipio()
            elif opcion == 2:
                self._consultar_por_busqueda_directa()
            elif opcion == 3:
                break

    def _consultar_por_municipio(self):
        """Selecciona municipio y localidad con coordenadas válidas para consultar el clima."""
        print("\n --- SELECCION DE MUNICIPIO ---")
        municipios = self.gestor_clima.municipios
        for i, mun in enumerate(municipios, start=1):
            print(f" {i}. {mun.nombre}")

        idx_mun = self.validar_entera(" Seleccione un municipio: ", 1, len(municipios)) - 1
        mun_sel = municipios[idx_mun]

        validas = mun_sel.localidades_con_coordenadas()
        if not validas:
            print(f"\n [!] El municipio '{mun_sel.nombre}' no posee localidades con coordenadas validas.")
            return

        print(f"\n --- LOCALIDADES CON COORDENADAS EN {mun_sel.nombre.upper()} ---")
        for i, loc in enumerate(validas, start=1):
            print(f" {i}. {loc.nombre} ({loc.latitud}, {loc.longitud})")

        idx_loc = self.validar_entera(" Seleccione una localidad: ", 1, len(validas)) - 1
        loc_sel = validas[idx_loc]

        print(f"\n [+] Consultando API de Open-Meteo para {loc_sel.nombre}...")
        clima = self.gestor_clima.consultar_clima_localidad(loc_sel, mun_sel)
        if clima:
            self._mostrar_detalles_clima(mun_sel.nombre, loc_sel, clima)

    def _consultar_por_busqueda_directa(self):
        """Permite ingresar un texto y filtrar localidades con coordenadas válidas."""
        termino = input("\n Ingrese el nombre (o parte) de la localidad: ").strip()
        if not termino:
            print(" [!] Debe ingresar al menos un caracter para realizar la busqueda.")
            return

        coincidencias = self.gestor_clima.buscar_localidades_por_nombre(termino)

        if not coincidencias:
            print(f"\n [!] No se encontraron localidades con coordenadas que contengan '{termino}'.")
            return

        print(f"\n --- COINCIDENCIAS ENCONTRADAS PARA '{termino}' ---")
        for i, (mun, loc) in enumerate(coincidencias, start=1):
            print(f" {i}. {loc.nombre} (Municipio: {mun.nombre})")

        selec = self.validar_entera(" Seleccione la localidad deseada: ", 1, len(coincidencias)) - 1
        mun_sel, loc_sel = coincidencias[selec]

        print(f"\n [+] Consultando API de Open-Meteo para {loc_sel.nombre} ({mun_sel.nombre})...")
        clima = self.gestor_clima.consultar_clima_localidad(loc_sel, mun_sel)
        if clima:
            self._mostrar_detalles_clima(mun_sel.nombre, loc_sel, clima)

    def _mostrar_detalles_clima(self, nombre_municipio, localidad, clima):
        """Despliega en pantalla los 6 detalles meteorológicos requeridos (Requerimiento 2.b.i-vi)."""
        print("\n" + "=" * 50)
        print(" REPORTE METEOROLOGICO EN TIEMPO REAL")
        print("=" * 50)
        print(f" i.   Municipio y Localidad: {nombre_municipio} - {localidad.nombre}")
        print(f" ii.  Coordenadas:            Lat: {localidad.latitud}, Lon: {localidad.longitud}")
        print(f" iii. Temperatura Actual:     {clima.temperatura} °C")
        print(f" iv.  Humedad Relativa:       {clima.humedad} %")
        print(f" v.   Velocidad del Viento:   {clima.velocidad_viento} km/h")
        print(f" vi.  Estado del Tiempo:      {clima.obtener_estado_texto()} (Codigo WMO: {clima.codigo_wmo})")
        print("=" * 50)

    def menu_estadisticas_sesion(self):
        """Modulo de estadísticas y reportes de la sesión activa (Requerimiento 3)."""
        while True:
            print("\n --- REPORTES Y ESTADISTICAS DE SESION ---")
            print(" 1. Ranking de Temperatura (Localidad mas calida y mas fria)")
            print(" 2. Cobertura Geografica (Localidades sin coordenadas / null)")
            print(" 3. Promedio General de temperatura de la sesion")
            print(" 4. Volver al menu principal")

            opcion = self.validar_entera(" Seleccione una opcion (1-4): ", 1, 4)

            if opcion == 1:
                calida, fria = self.gestor_clima.obtener_ranking_temperatura()
                print("\n RANKING DE TEMPERATURA DE LA SESION:")
                if calida:
                    print(f"  [+] Mas Calida: {calida.nombre} con {calida.clima_actual.temperatura} °C")
                else:
                    print("  [+] Mas Calida: Sin datos de consulta en esta sesion.")

                if fria:
                    print(f"  [-] Mas Fria:   {fria.nombre} con {fria.clima_actual.temperatura} °C")
                else:
                    print("  [-] Mas Fria:   Sin datos de consulta en esta sesion.")

            elif opcion == 2:
                print("\n LOCALIDADES SIN COORDENADAS REGISTRADAS (NULL) AGRUPADAS POR MUNICIPIO:")
                cobertura = self.gestor_clima.obtener_cobertura_geografica_null()
                for mun, sin_coords in cobertura:
                    print(f"\n [-] Municipio: {mun.nombre} ({len(sin_coords)} localidades sin coords)")
                    if sin_coords:
                        for loc in sin_coords:
                            print(f"    |- {loc.nombre}")
                    else:
                        print("    |- Todas sus localidades poseen coordenadas geograficas.")

            elif opcion == 3:
                promedio = self.gestor_clima.obtener_promedio_temperatura_sesion()
                print(f"\n [+] Promedio General de Temperatura en la Sesion Activa: {promedio} °C")

            elif opcion == 4:
                break

    def menu_historico(self):
        """Módulo de análisis histórico y generación de gráficos (Requerimiento 4)."""
        print("\n --- ANALISIS HISTORICO Y EVOLUCION CLIMATICA ---")
        
        # Seleccionar localidad con coordenadas
        coincidencias = []
        for mun in self.gestor_clima.municipios:
            for loc in mun.localidades_con_coordenadas():
                coincidencias.append((mun, loc))

        if not coincidencias:
            print(" [!] No existen localidades con coordenadas para consultar historicos.")
            return

        print("\n Seleccione la localidad a analizar:")
        for i, (mun, loc) in enumerate(coincidencias, start=1):
            print(f" {i}. {loc.nombre} ({mun.nombre})")

        idx_sel = self.validar_entera(" Seleccione una localidad: ", 1, len(coincidencias)) - 1
        mun_sel, loc_sel = coincidencias[idx_sel]

        print("\n Indique el periodo de tiempo a analizar (formato AAAA-MM-DD):")
        fecha_inicio = self.validar_fecha(" Fecha de inicio (ej. 2023-01-01): ")
        fecha_fin = self.validar_fecha(" Fecha de fin    (ej. 2023-12-31): ")

        # Validamos que la fecha de inicio no sea mayor a la de fin
        if fecha_inicio > fecha_fin:
            print("\n [!] Error: La fecha de inicio no puede ser posterior a la fecha de fin.")
            return

        print(f"\n [+] Procesando datos historicos para {loc_sel.nombre} entre {fecha_inicio} y {fecha_fin}...")
        registros, promedios, extremos = self.gestor_historico.consultar_historico(
            loc_sel, fecha_inicio, fecha_fin
        )

        if not registros:
            print(" [!] No se pudieron procesar los datos historicos para ese periodo.")
            return

        # 4.a Mostrar registros por cada mes
        print("\n" + "=" * 65)
        print(f" REGISTROS METEOROLOGICOS MENSUALES - {loc_sel.nombre.upper()}")
        print("=" * 65)
        for r in registros:
            print(r)
            print("-" * 65)

        # 4.b Mostrar promedios generales
        print("\n VALORES PROMEDIO DEL PERIODO:")
        print(f"  |- Temperatura promedio:    {promedios['temperatura']} °C")
        print(f"  |- Humedad relativa:        {promedios['humedad']} %")
        print(f"  |- Precipitación promedio:  {promedios['precipitacion']} mm")
        print(f"  |- Velocidad viento:        {promedios['velocidad_viento']} km/h")

        # 4.c Mostrar resumen de extremos por año
        print("\n REGISTROS EXTREMOS POR AÑO EN EL PERIODO:")
        print(f"  |- Año mas caluroso:                  {extremos['caluroso']}")
        print(f"  |- Año mas fresco:                    {extremos['fresco']}")
        print(f"  |- Año con mayor precipitacion:       {extremos['precipitacion']}")
        print(f"  |- Año con mayor humedad relativa:    {extremos['humedad']}")
        print("=" * 65)

        # 4.d Opción de mostrar gráfico comparativo con Matplotlib
        ver_grafico = input("\n Desea desplegar el grafico comparativo en pantalla? (s/n): ").strip().lower()
        if ver_grafico == 's':
            print(" Desplegando grafico...")
            self.gestor_historico.generar_grafico_historico(registros, loc_sel.nombre)
