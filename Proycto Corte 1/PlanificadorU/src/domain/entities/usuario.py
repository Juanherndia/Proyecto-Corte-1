"""
Entidad Usuario - Domain Layer
Representa un usuario del sistema médico con sus atributos y reglas de negocio.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RolUsuario(Enum):
    """Roles disponibles en el sistema médico"""
    MEDICO = "medico"
    ENFERMERO = "enfermero"
    ADMINISTRADOR = "administrador"
    RESIDENTE = "residente"


class EstadoUsuario(Enum):
    """Estados posibles de un usuario"""
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"


@dataclass
class Usuario:
    """
    Entidad Usuario del dominio médico.
    Cumple con SRP: Solo maneja lógica relacionada con usuarios.
    """
    id: Optional[str]
    email: str
    nombre: str
    apellido: str
    especialidad: Optional[str]
    numero_licencia: str
    telefono: str
    rol: RolUsuario
    estado: EstadoUsuario
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    ultimo_acceso: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones de dominio"""
        if not self.email or "@" not in self.email:
            raise ValueError("Email inválido")
        
        if not self.numero_licencia:
            raise ValueError("Número de licencia médica es requerido")
        
        if len(self.nombre.strip()) < 2:
            raise ValueError("Nombre debe tener al menos 2 caracteres")
    
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    def es_medico(self) -> bool:
        """Verifica si el usuario es médico"""
        return self.rol in [RolUsuario.MEDICO, RolUsuario.RESIDENTE]
    
    def puede_gestionar_emergencias(self) -> bool:
        """Determina si el usuario puede gestionar emergencias"""
        return self.rol in [RolUsuario.MEDICO, RolUsuario.ADMINISTRADOR]
    
    def activar(self):
        """Activa el usuario"""
        self.estado = EstadoUsuario.ACTIVO
        self.fecha_actualizacion = datetime.now()
    
    def desactivar(self):
        """Desactiva el usuario"""
        self.estado = EstadoUsuario.INACTIVO
        self.fecha_actualizacion = datetime.now()
    
    def registrar_acceso(self):
        """Registra el último acceso del usuario"""
        self.ultimo_acceso = datetime.now()