class Localidad:
    """Clase que representa una zona/sector geográfico de un municipio."""

    def __init__(self, nombre, latitud=None, longitud=None):
        # Nombre oficial de la localidad (ej. "La Candelaria", "Petare")
        self.nombre = nombre
        
        # Coordenada de latitud (float o None si no vino en el JSON)
        self.latitud = latitud
        
        # Coordenada de longitud (float o None si no vino en el JSON)
        self.longitud = longitud
        
        # Atributo para almacenar un objeto ClimaActual cuando el usuario haga una consulta
        self.clima_actual = None

    def tiene_coordenadas(self):
        """Evalúa si la localidad cuenta con latitud y longitud válidas para llamar a la API."""
        # Retorna True únicamente si AMBAS coordenadas son distintas de None
        return self.latitud is not None and self.longitud is not None

    def show(self):
        """Muestra en pantalla el detalle completo de la localidad y su clima si lo tiene."""
        # Operador ternario para formatear la cadena de coordenadas o indicar que es NULL
        coords = f"({self.latitud}, {self.longitud})" if self.tiene_coordenadas() else "[Sin coordenadas]"
        print(f"📍 Localidad: {self.nombre} | Coordenadas: {coords}")
        
        # Verificamos si ya se le asignó un clima a esta localidad
        if self.clima_actual:
            print("   └─ Clima asignado:")
            # Llamamos al método de la instancia ClimaActual para mostrar los datos
            self.clima_actual.mostrar_reporte_corto()
        else:
            print("   └─ Clima: No consultado aún")

    def __str__(self):
        """Representación formal en texto del objeto Localidad."""
        coord_status = f"({self.latitud}, {self.longitud})" if self.tiene_coordenadas() else "(Sin coordenadas)"
        return f"Localidad: {self.nombre} {coord_status}"