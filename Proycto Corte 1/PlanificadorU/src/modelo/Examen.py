from .Evento import Evento

class Examen(Evento):
    """Representa un examen académico."""
    def __init__(self, nombre, fecha, hora, materia):
        super().__init__(nombre, fecha, hora)
        self.materia = materia

    def mostrar_info(self):
        return f"Examen: {self.nombre} - Fecha: {self.fecha} - Hora: {self.hora} - Materia: {self.materia}"
