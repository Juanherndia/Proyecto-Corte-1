"""
Repositorio de Usuarios - Domain Layer Interface
Define el contrato para la persistencia de usuarios.
Cumple con DIP: Interfaz en el dominio, implementación en infraestructura.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.usuario import Usuario, RolUsuario, EstadoUsuario


class IUsuarioRepository(ABC):
    """
    Interfaz del repositorio de usuarios.
    Aplica ISP: Interfaz específica para operaciones de usuario.
    """
    
    @abstractmethod
    async def crear(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario"""
        pass
    
    @abstractmethod
    async def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """Busca un usuario por ID"""
        pass
    
    @abstractmethod
    async def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por email"""
        pass
    
    @abstractmethod
    async def buscar_por_licencia(self, numero_licencia: str) -> Optional[Usuario]:
        """Busca un usuario por número de licencia"""
        pass
    
    @abstractmethod
    async def actualizar(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente"""
        pass
    
    @abstractmethod
    async def eliminar(self, id: str) -> bool:
        """Elimina un usuario por ID"""
        pass
    
    @abstractmethod
    async def listar_por_rol(self, rol: RolUsuario) -> List[Usuario]:
        """Lista usuarios por rol"""
        pass
    
    @abstractmethod
    async def listar_por_estado(self, estado: EstadoUsuario) -> List[Usuario]:
        """Lista usuarios por estado"""
        pass
    
    @abstractmethod
    async def listar_por_especialidad(self, especialidad: str) -> List[Usuario]:
        """Lista usuarios por especialidad médica"""
        pass
    
    @abstractmethod
    async def contar_usuarios_activos(self) -> int:
        """Cuenta usuarios activos"""
        pass
    
    @abstractmethod
    async def verificar_email_existe(self, email: str, excluir_id: Optional[str] = None) -> bool:
        """Verifica si un email ya existe"""
        pass