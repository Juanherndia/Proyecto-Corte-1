from ..modelo.Tarea import Tarea
from ..modelo.Examen import Examen
from ..modelo.Evento import Evento

class EventoFactory:
    """Factory Method para crear eventos."""
    @staticmethod
    def crear_evento(tipo, **kwargs):
        if tipo == "tarea":
            return Tarea(**kwargs)
        elif tipo == "examen":
            return Examen(**kwargs)
        else:
            return Evento(**kwargs)
