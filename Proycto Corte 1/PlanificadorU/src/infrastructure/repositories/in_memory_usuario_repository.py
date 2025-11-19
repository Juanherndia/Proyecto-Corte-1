"""
Implementación en memoria del repositorio de usuarios.
Para desarrollo y testing. En producción se reemplazaría por base de datos.
Cumple con DIP: Implementa la interfaz del dominio.
"""
from typing import List, Optional, Dict
import uuid
from datetime import datetime
from ...domain.entities.usuario import Usuario, RolUsuario, EstadoUsuario
from ...domain.repositories.usuario_repository import IUsuarioRepository


class InMemoryUsuarioRepository(IUsuarioRepository):
    """
    Implementación en memoria del repositorio de usuarios.
    Aplica LSP: Puede sustituir la interfaz sin cambiar comportamiento.
    """
    
    def __init__(self):
        self._usuarios: Dict[str, Usuario] = {}
        self._usuario_por_email: Dict[str, str] = {}
        self._usuario_por_licencia: Dict[str, str] = {}
    
    async def crear(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario"""
        # Generar ID si no existe
        if not usuario.id:
            usuario.id = str(uuid.uuid4())
        
        # Verificar unicidad de email
        if usuario.email.lower() in self._usuario_por_email:
            raise ValueError("El email ya está registrado")
        
        # Verificar unicidad de licencia
        if usuario.numero_licencia in self._usuario_por_licencia:
            raise ValueError("El número de licencia ya está registrado")
        
        # Almacenar usuario
        self._usuarios[usuario.id] = usuario
        self._usuario_por_email[usuario.email.lower()] = usuario.id
        self._usuario_por_licencia[usuario.numero_licencia] = usuario.id
        
        return usuario
    
    async def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """Busca un usuario por ID"""
        return self._usuarios.get(id)
    
    async def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por email"""
        usuario_id = self._usuario_por_email.get(email.lower())
        return self._usuarios.get(usuario_id) if usuario_id else None
    
    async def buscar_por_licencia(self, numero_licencia: str) -> Optional[Usuario]:
        """Busca un usuario por número de licencia"""
        usuario_id = self._usuario_por_licencia.get(numero_licencia)
        return self._usuarios.get(usuario_id) if usuario_id else None
    
    async def actualizar(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente"""
        if not usuario.id or usuario.id not in self._usuarios:
            raise ValueError("Usuario no encontrado")
        
        # Verificar si cambió el email
        usuario_actual = self._usuarios[usuario.id]
        if usuario.email.lower() != usuario_actual.email.lower():
            # Actualizar índice de email
            del self._usuario_por_email[usuario_actual.email.lower()]
            self._usuario_por_email[usuario.email.lower()] = usuario.id
        
        # Actualizar usuario
        usuario.fecha_actualizacion = datetime.now()
        self._usuarios[usuario.id] = usuario
        
        return usuario
    
    async def eliminar(self, id: str) -> bool:
        """Elimina un usuario por ID"""
        if id not in self._usuarios:
            return False
        
        usuario = self._usuarios[id]
        
        # Limpiar índices
        del self._usuario_por_email[usuario.email.lower()]
        del self._usuario_por_licencia[usuario.numero_licencia]
        del self._usuarios[id]
        
        return True
    
    async def listar_por_rol(self, rol: RolUsuario) -> List[Usuario]:
        """Lista usuarios por rol"""
        return [
            usuario for usuario in self._usuarios.values()
            if usuario.rol == rol
        ]
    
    async def listar_por_estado(self, estado: EstadoUsuario) -> List[Usuario]:
        """Lista usuarios por estado"""
        return [
            usuario for usuario in self._usuarios.values()
            if usuario.estado == estado
        ]
    
    async def listar_por_especialidad(self, especialidad: str) -> List[Usuario]:
        """Lista usuarios por especialidad médica"""
        return [
            usuario for usuario in self._usuarios.values()
            if usuario.especialidad and usuario.especialidad.lower() == especialidad.lower()
        ]
    
    async def contar_usuarios_activos(self) -> int:
        """Cuenta usuarios activos"""
        return len([
            usuario for usuario in self._usuarios.values()
            if usuario.estado == EstadoUsuario.ACTIVO
        ])
    
    async def verificar_email_existe(self, email: str, excluir_id: Optional[str] = None) -> bool:
        """Verifica si un email ya existe"""
        usuario_id = self._usuario_por_email.get(email.lower())
        if not usuario_id:
            return False
        
        return usuario_id != excluir_id if excluir_id else True
    
    def limpiar(self):
        """Limpia todos los datos (para testing)"""
        self._usuarios.clear()
        self._usuario_por_email.clear()
        self._usuario_por_licencia.clear()
    
    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios (para debugging)"""
        return list(self._usuarios.values())
    
    async def inicializar_datos_prueba(self):
        """Inicializa datos de prueba"""
        usuarios_prueba = [
            Usuario(
                id=None,
                email="admin@hospital.com",
                nombre="Admin",
                apellido="Sistema",
                especialidad=None,
                numero_licencia="ADMIN001",
                telefono="1234567890",
                rol=RolUsuario.ADMINISTRADOR,
                estado=EstadoUsuario.ACTIVO,
                fecha_creacion=datetime.now()
            ),
            Usuario(
                id=None,
                email="dr.garcia@hospital.com",
                nombre="Carlos",
                apellido="García",
                especialidad="Cardiología",
                numero_licencia="MED001",
                telefono="1234567891",
                rol=RolUsuario.MEDICO,
                estado=EstadoUsuario.ACTIVO,
                fecha_creacion=datetime.now()
            ),
            Usuario(
                id=None,
                email="dra.martinez@hospital.com",
                nombre="Ana",
                apellido="Martínez",
                especialidad="Urgencias",
                numero_licencia="MED002",
                telefono="1234567892",
                rol=RolUsuario.MEDICO,
                estado=EstadoUsuario.ACTIVO,
                fecha_creacion=datetime.now()
            ),
            Usuario(
                id=None,
                email="enf.lopez@hospital.com",
                nombre="María",
                apellido="López",
                especialidad="Enfermería General",
                numero_licencia="ENF001",
                telefono="1234567893",
                rol=RolUsuario.ENFERMERO,
                estado=EstadoUsuario.ACTIVO,
                fecha_creacion=datetime.now()
            )
        ]
        
        for usuario in usuarios_prueba:
            await self.crear(usuario)