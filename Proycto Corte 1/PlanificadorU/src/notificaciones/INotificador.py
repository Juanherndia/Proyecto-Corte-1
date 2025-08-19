from abc import ABC, abstractmethod

class INotificador(ABC):
    """Interfaz para notificaciones."""
    @abstractmethod
    def notificar(self, mensaje):
        pass
