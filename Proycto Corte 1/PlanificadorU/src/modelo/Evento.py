class Evento:
    """Clase base para eventos en el calendario."""
    def __init__(self, nombre, fecha, hora):
        self.nombre = nombre
        self.fecha = fecha
        self.hora = hora

    def mostrar_info(self):
        return f"Evento: {self.nombre} - Fecha: {self.fecha} - Hora: {self.hora}"
