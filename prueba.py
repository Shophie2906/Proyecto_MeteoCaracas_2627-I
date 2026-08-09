from core.gestor_datos import GestorDatos
from core.api_client import APIClient

# 1. Cargar las zonas desde el JSON
municipios = GestorDatos.cargar_datos("zonas_caracas.json")

# 2. Probar la API con una localidad real (ejemplo: Altamira en Chacao)
if municipios:
    chacao = municipios[0] # Municipio Chacao
    altamira = chacao.localidades[0] # Localidad Altamira
    
    print(f"\n🌐 Consultando API en tiempo real para: {altamira.nombre}...")
    reporte = APIClient.obtener_clima_localidad(altamira)
    
    if reporte:
        print(f"✅ ¡Conexión Exitosa! Datos en vivo: {reporte}")