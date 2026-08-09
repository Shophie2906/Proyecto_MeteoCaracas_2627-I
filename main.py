from db.json_loader import JSONLoader
from tools.gestor_clima import GestorClima
from tools.gestor_historico import GestorHistorico

#  Si tu archivo es interfaz.py úsalo en minúsculas. Si lo guardaste como Interfaz.py, pon: from Interfaz import Interfaz
from Interfaz import Interfaz 

def main():
    """Punto de entrada principal para ejecutar la aplicación MeteoCaracas."""
    print("Iniciando Sistema MeteoCaracas...")
    
    # 1. Carga de datos desde zonas_caracas.json
    municipios = JSONLoader.cargar_zonas("data/zonas_caracas.json")
    if not municipios:
        print("Error crítico: No se pudieron cargar los datos de municipios y localidades.")
        return

    # 2. Instanciación de controladores
    gestor_clima = GestorClima(municipios)
    gestor_historico = GestorHistorico()

    # 3. Instanciación de la interfaz por consola
    interfaz = Interfaz(gestor_clima, gestor_historico)

    # 4. Presentación automática del reporte inicial de carga (Requerimiento 1)
    interfaz.mostrar_reporte_carga_inicial()

    # 5. Ejecución del menú interactivo principal
    interfaz.Start()

if __name__ == "__main__":
    main()
