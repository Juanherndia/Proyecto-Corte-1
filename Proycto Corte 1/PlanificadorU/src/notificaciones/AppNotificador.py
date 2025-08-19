from .INotificador import INotificador

class AppNotificador(INotificador):
    def notificar(self, mensaje):
        print(f"Notificación en la app: {mensaje}")
