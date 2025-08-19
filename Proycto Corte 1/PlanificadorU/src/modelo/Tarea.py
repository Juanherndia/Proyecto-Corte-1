from .Evento import Evento

class Tarea(Evento):
    """Representa una tarea académica."""
    def __init__(self, nombre, fecha, hora, descripcion):
        super().__init__(nombre, fecha, hora)
        self.descripcion = descripcion

    def mostrar_info(self):
        return f"Tarea: {self.nombre} - Fecha: {self.fecha} - Hora: {self.hora} - Descripción: {self.descripcion}"
