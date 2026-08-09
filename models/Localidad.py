class Localidad:

    def __init__(self, nombre, latitud=None, longitud=None):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.clima_actual = None

    def tiene_coordenadas(self):
        return self.latitud is not None and self.longitud is not None

    def show(self):
        coords = f"({self.latitud}, {self.longitud})" if self.tiene_coordenadas() else "[Sin coordenadas]"
        print(f"📍 Localidad: {self.nombre} | Coordenadas: {coords}")
        if self.clima_actual:
            print("   └─ Clima asignado:")
            self.clima_actual.mostrar_reporte_corto()
        else:
            print("   └─ Clima: No consultado aún")

    def __str__(self):
        coord_status = f"({self.latitud}, {self.longitud})" if self.tiene_coordenadas() else "(Sin coordenadas)"
        return f"Localidad: {self.nombre} {coord_status}"