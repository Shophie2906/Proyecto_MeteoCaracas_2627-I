from models.Estadisticas import Estadisticas
from models.ClimaActual import ClimaActual
from models.Localidad import Localidad
from models.Municipio import Municipio
from models.RegistroHistorico import RegistroHistorico

class Interfaz:
    ''' Gestiona el menu interactivo, la nagevacion y las validadiones de usuario'''
    def __init__(self, municipios, estadisticas):
      self.municipios = municipios
      self.estadisticas = estadisticas
      
    def validar_entera(self, mensaje, minimo, maximo):
        while True:
            try: 
                opcion = int(input(mensaje))
                if minimo <= opcion <= maximo:
                    return opcion
                print(f" Error! Ingresa un numero entre {minimo} y {maximo}")
            except ValueError: 
                print("Error! Por favor ingresa un numero valido")
      
    def Start(self):
        '''Ejecuta el menu principal del sistema en un bucle continuo'''
        while True:
            print()
            print(" Bienvenido al Sistema Meterologico MeteoCaracas!")  
            print(" Seleccione alguna opcion:")
            print("\t 1- Reporte incial de carga inicial de localidades")
            print("\t 2- Consulta del clima en tiempo real")
            print("\t 3- Reportes y estadisticas de sesion")
            print("\t 4- Analisis historico")
            print("\t 5- Salir del programa")
            
            opcion = int(input("Indique su eleccion (1-5): "))
            
            if opcion == 1:
                self.menu_reporte_carga()
            elif opcion == 2:
                pass
            elif opcion == 3:
                pass
            elif opcion == 4:
                pass
            elif opcion == 5:
                print()
                print("\n Gracias por utilizar MeteoCaracas!!")
                print("Hasta luego. \n")
                break
            
    def menu_reporte_carga(self):
        print()
        print("Reporte de cobertura de carga inicial: ")
        print()
        for municipio in self.municipios:
            print(f" Municipio: {municipio.nombre}")
            print(f"\t Localidades cargadas: {municipio.total_localidades()}")
            print(f"\t Con coordenadas: {len(municipio.localidades_con_coordenadas())}")
            print(f"\t Sin coordenadas: {len(municipio.localidades_sin_coordenadas())}")
            print(f"\t Cobertura:{municipio.porcentaje_con_coordenadas()}%")
        print()   
        
    def menu_consulta_tiempo_real(self):
        print()
        print("--------- Consulta del clima en tiempo real ---------")
        print("\t 1- Consultar por municipio y localidad")
        print("\t 2- Busqueda directa por Localidad (nombre)")
        print("\t 3- Volver al menu principal")
        
        consulta = self.validar_entera("Seleccione la modalidad de consulta (1-3): ", 1, 3)
        
        if consulta == 1: 
            pass
        elif consulta == 2:
            pass
        
    def consultar_por_municipio_y_localidad(self):
        '''Permite seleccionar municipio y localidad con coordenadas para la consulta.'''
        
        print(" --- Seleccion de Municipio ---")
        for idx, mun in enumerate(self.municipios, start=1):
            print(f"{idx}. {mun.nombre}")
            
        idx_mun = self.validar_entera("seleccione un municipio: ", 1, len(self.municipios)) - 1
        municipio_seleccionado = self.municipios[idx_mun]
        
        validas = municipio_seleccionado.localidades_con_coordenadas()
        if not validas:
            print(f"\n El municipio {municipio_seleccionado.nombre} no tiene localidades con coordenadas validas.")
            input(" Presione ENTER para continuar.")
            return
        
        print(f"--- Localidades en {municipio_seleccionado.nombre.upper()} ---")
        for idx, loc in enumerate(validas, start=1):
            print(f"{idx}. {loc.nombre}")
            
        idx_loc = self.validar_entera("seleccione una localidad: ", 1, len(validas)) - 1
        Localidad_seleccionada = validas[idx_loc]    
        
        print(f"\n Consultando API Open-Meteo para: {Localidad_seleccionada.nombre}...")
        
    def consultar_por_busqueda_directa(self) -> None:
        '''Permite ingresar un texto para filtrar localidades coincidentes.'''
        
        termino = input(" Ingrese el nombre (o parte del nombre) de la localidad: ").strip().lower()
        if not termino:
            print(" Debe ingresar al menos un caracter para buscar.")
            return
        
        coincidencias = []
        for mun in self.municipios:
            for loc in mun.localidades_con_coordenadas():
                if termino in loc.nombre.lower():
                    coincidencias.append((mun, loc))
                    
        if not coincidencias: 
            print(f"\n No se encontraron localidades con coordenadas validas que coincidan con '{termino}'.")
            input(" Presione ENTER para continuar.")
            return
        
        print("\n --- COINCIDENCIAS ENCONTRADAS ---")
        for idx, (mun, loc) in enumerate(coincidencias, start=1):
            print(f"{idx}. {loc.nombre} ({mun.nombre})")
                               
        selec = self.validar_entera(" Seleccione la localidad deseada: ", 1, len(coincidencias)) - 1
        mun_sel, loc_sel = coincidencias[selec]
        
        print(f"\n Consultado API Open-Meteo para: {loc_sel.nombre} ({mun_sel.nombre})...")
        
    def menu_estadisticas_sesion(self):
        print()
        print("----- Reporte y Estadisticas de Sesion -----")
        print("\t 1- Ranking de temperatura (Mas calida y mas fria)")
        print("\t 2- Cobertura Geografica (Localidades sin coordenadas registradas)")
        print("\t 3- Promedio General de Temperatura en la sesion")
        print("\t 4- Volver al menu principal")
        
        opcion = self.validar_entera("Seleccione la opcion deseada (1-4): ",1, 4)
        
        if opcion == 1:
            print(self.estadisticas)
        elif opcion == 2:
            print()
            print(" LOCALIDADES SIN COORDENADAS REGISTRADAS (NULL)")    
            print()
            for mun in self.municipios:
                sin_coords = [loc for loc in mun.localidades if not loc.tiene_coordenadas()]
                print(f" Municipio: {mun.nombre} ({len(sin_coords)} localidades)")
                if sin_coords:
                    for loc in sin_coords:
                        print(f"\t {loc.nombre}")
                else: 
                    print("\t Todas sus localidades poseen coordenadas")
                    
            input("\n Presione ENTER para continuar...")
            
    def menu_historico(self):
        '''Muestra el modulo de analisis historico.'''
        print("\n --- Analisis Historico y Evolucion Climatica ---")
        print(" Modulo de historicos en proceso de integracion")
        input("\n Presione ENTER para continuar...")
                        