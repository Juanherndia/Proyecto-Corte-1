class Horario:
    """Gestiona las franjas de tiempo del usuario."""
    def __init__(self):
        self.franjas = []

    def agregar_franja(self, inicio, fin):
        self.franjas.append((inicio, fin))

    def mostrar_horario(self):
        return self.franjas
