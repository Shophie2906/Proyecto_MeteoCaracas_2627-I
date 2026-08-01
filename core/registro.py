from datetime import datetime
from models.estacion import Registro

def pedir_numero(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingresa un numero valido.")

def registrar_datos():
    print("\n--- Nuevo Registro Meteorologico ---")
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"Fecha de registro: {fecha_actual}")

    temp = pedir_numero("Temperatura (C): ")
    hum = pedir_numero("Humedad (%): ")
    presion = pedir_numero("Presion (hPa): ")
    lluvia = pedir_numero("Lluvia (mm): ")

    nuevo = Registro(fecha_actual, temp, hum, presion, lluvia)
    print("¡Registro guardado con exito!")
    return nuevo