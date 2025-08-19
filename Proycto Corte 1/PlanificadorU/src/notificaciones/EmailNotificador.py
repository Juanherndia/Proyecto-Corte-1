from .INotificador import INotificador

class EmailNotificador(INotificador):
    def notificar(self, mensaje):
        print(f"Enviando email: {mensaje}")
