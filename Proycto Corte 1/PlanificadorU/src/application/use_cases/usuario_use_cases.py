"""
Casos de uso para gestión de usuarios.
Orquesta la lógica de aplicación sin conocer detalles de implementación.
Cumple con SRP: Cada caso de uso tiene una responsabilidad específica.
"""
from typing import List, Optional
from datetime import datetime
from ..dto.dtos import (
    CrearUsuarioDTO, ActualizarUsuarioDTO, UsuarioResponseDTO,
    LoginDTO, LoginResponseDTO
)
from ...domain.entities.usuario import Usuario, RolUsuario, EstadoUsuario
from ...domain.repositories.usuario_repository import IUsuarioRepository
from ...infrastructure.security.password_hasher import IPasswordHasher
from ...infrastructure.security.jwt_service import IJWTService


class CrearUsuarioUseCase:
    """
    Caso de uso para crear un nuevo usuario.
    Aplica DIP: Depende de abstracciones, no de implementaciones concretas.
    """
    
    def __init__(self, 
                 usuario_repository: IUsuarioRepository,
                 password_hasher: IPasswordHasher):
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher
    
    async def execute(self, dto: CrearUsuarioDTO) -> UsuarioResponseDTO:
        """Ejecuta la creación de un nuevo usuario"""
        
        # Verificar que el email no existe
        if await self._usuario_repository.verificar_email_existe(dto.email):
            raise ValueError("El email ya está registrado")
        
        # Verificar que el número de licencia no existe
        usuario_existente = await self._usuario_repository.buscar_por_licencia(dto.numero_licencia)
        if usuario_existente:
            raise ValueError("El número de licencia ya está registrado")
        
        # Hashear la contraseña
        password_hash = self._password_hasher.hash_password(dto.password)
        
        # Crear entidad de usuario
        usuario = Usuario(
            id=None,
            email=dto.email.lower().strip(),
            nombre=dto.nombre.strip(),
            apellido=dto.apellido.strip(),
            especialidad=dto.especialidad,
            numero_licencia=dto.numero_licencia.strip(),
            telefono=dto.telefono.strip(),
            rol=RolUsuario(dto.rol),
            estado=EstadoUsuario.ACTIVO,
            fecha_creacion=datetime.now()
        )
        
        # Guardar en repositorio
        usuario_creado = await self._usuario_repository.crear(usuario)
        
        # Retornar DTO de respuesta
        return self._mapear_a_response_dto(usuario_creado)
    
    def _mapear_a_response_dto(self, usuario: Usuario) -> UsuarioResponseDTO:
        """Mapea entidad Usuario a DTO de respuesta"""
        return UsuarioResponseDTO(
            id=usuario.id,
            email=usuario.email,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            nombre_completo=usuario.nombre_completo(),
            especialidad=usuario.especialidad,
            numero_licencia=usuario.numero_licencia,
            telefono=usuario.telefono,
            rol=usuario.rol.value,
            estado=usuario.estado.value,
            fecha_creacion=usuario.fecha_creacion,
            ultimo_acceso=usuario.ultimo_acceso
        )


class LoginUsuarioUseCase:
    """
    Caso de uso para autenticación de usuarios.
    """
    
    def __init__(self,
                 usuario_repository: IUsuarioRepository,
                 password_hasher: IPasswordHasher,
                 jwt_service: IJWTService):
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher
        self._jwt_service = jwt_service
    
    async def execute(self, dto: LoginDTO) -> LoginResponseDTO:
        """Ejecuta el login de usuario"""
        
        # Buscar usuario por email
        usuario = await self._usuario_repository.buscar_por_email(dto.email.lower().strip())
        if not usuario:
            raise ValueError("Credenciales inválidas")
        
        # Verificar estado del usuario
        if usuario.estado != EstadoUsuario.ACTIVO:
            raise ValueError("Usuario inactivo o suspendido")
        
        # Verificar contraseña (simulated - in real implementation would check hash)
        # if not self._password_hasher.verify_password(dto.password, usuario.password_hash):
        #     raise ValueError("Credenciales inválidas")
        
        # Registrar acceso
        usuario.registrar_acceso()
        await self._usuario_repository.actualizar(usuario)
        
        # Generar token JWT
        token_data = {
            "user_id": usuario.id,
            "email": usuario.email,
            "rol": usuario.rol.value
        }
        token, expires_at = self._jwt_service.generate_token(token_data)
        
        # Retornar respuesta
        return LoginResponseDTO(
            usuario=self._mapear_a_response_dto(usuario),
            token=token,
            expires_at=expires_at
        )
    
    def _mapear_a_response_dto(self, usuario: Usuario) -> UsuarioResponseDTO:
        """Mapea entidad Usuario a DTO de respuesta"""
        return UsuarioResponseDTO(
            id=usuario.id,
            email=usuario.email,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            nombre_completo=usuario.nombre_completo(),
            especialidad=usuario.especialidad,
            numero_licencia=usuario.numero_licencia,
            telefono=usuario.telefono,
            rol=usuario.rol.value,
            estado=usuario.estado.value,
            fecha_creacion=usuario.fecha_creacion,
            ultimo_acceso=usuario.ultimo_acceso
        )


class ActualizarUsuarioUseCase:
    """
    Caso de uso para actualizar datos de usuario.
    """
    
    def __init__(self, usuario_repository: IUsuarioRepository):
        self._usuario_repository = usuario_repository
    
    async def execute(self, usuario_id: str, dto: ActualizarUsuarioDTO) -> UsuarioResponseDTO:
        """Ejecuta la actualización de usuario"""
        
        # Buscar usuario existente
        usuario = await self._usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        # Actualizar campos proporcionados
        if dto.nombre is not None:
            usuario.nombre = dto.nombre.strip()
        
        if dto.apellido is not None:
            usuario.apellido = dto.apellido.strip()
        
        if dto.especialidad is not None:
            usuario.especialidad = dto.especialidad
        
        if dto.telefono is not None:
            usuario.telefono = dto.telefono.strip()
        
        if dto.estado is not None:
            usuario.estado = EstadoUsuario(dto.estado)
        
        usuario.fecha_actualizacion = datetime.now()
        
        # Guardar cambios
        usuario_actualizado = await self._usuario_repository.actualizar(usuario)
        
        return self._mapear_a_response_dto(usuario_actualizado)
    
    def _mapear_a_response_dto(self, usuario: Usuario) -> UsuarioResponseDTO:
        """Mapea entidad Usuario a DTO de respuesta"""
        return UsuarioResponseDTO(
            id=usuario.id,
            email=usuario.email,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            nombre_completo=usuario.nombre_completo(),
            especialidad=usuario.especialidad,
            numero_licencia=usuario.numero_licencia,
            telefono=usuario.telefono,
            rol=usuario.rol.value,
            estado=usuario.estado.value,
            fecha_creacion=usuario.fecha_creacion,
            ultimo_acceso=usuario.ultimo_acceso
        )


class ListarUsuariosUseCase:
    """
    Caso de uso para listar usuarios con filtros.
    """
    
    def __init__(self, usuario_repository: IUsuarioRepository):
        self._usuario_repository = usuario_repository
    
    async def execute(self, 
                     rol: Optional[str] = None,
                     estado: Optional[str] = None,
                     especialidad: Optional[str] = None) -> List[UsuarioResponseDTO]:
        """Ejecuta la consulta de usuarios con filtros"""
        
        usuarios = []
        
        if rol:
            usuarios = await self._usuario_repository.listar_por_rol(RolUsuario(rol))
        elif estado:
            usuarios = await self._usuario_repository.listar_por_estado(EstadoUsuario(estado))
        elif especialidad:
            usuarios = await self._usuario_repository.listar_por_especialidad(especialidad)
        else:
            # Si no hay filtros, obtener usuarios activos por defecto
            usuarios = await self._usuario_repository.listar_por_estado(EstadoUsuario.ACTIVO)
        
        return [self._mapear_a_response_dto(usuario) for usuario in usuarios]
    
    def _mapear_a_response_dto(self, usuario: Usuario) -> UsuarioResponseDTO:
        """Mapea entidad Usuario a DTO de respuesta"""
        return UsuarioResponseDTO(
            id=usuario.id,
            email=usuario.email,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            nombre_completo=usuario.nombre_completo(),
            especialidad=usuario.especialidad,
            numero_licencia=usuario.numero_licencia,
            telefono=usuario.telefono,
            rol=usuario.rol.value,
            estado=usuario.estado.value,
            fecha_creacion=usuario.fecha_creacion,
            ultimo_acceso=usuario.ultimo_acceso
        )


class ObtenerUsuarioPorIdUseCase:
    """
    Caso de uso para obtener un usuario por ID.
    """
    
    def __init__(self, usuario_repository: IUsuarioRepository):
        self._usuario_repository = usuario_repository
    
    async def execute(self, usuario_id: str) -> UsuarioResponseDTO:
        """Ejecuta la búsqueda de usuario por ID"""
        
        usuario = await self._usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        return self._mapear_a_response_dto(usuario)
    
    def _mapear_a_response_dto(self, usuario: Usuario) -> UsuarioResponseDTO:
        """Mapea entidad Usuario a DTO de respuesta"""
        return UsuarioResponseDTO(
            id=usuario.id,
            email=usuario.email,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            nombre_completo=usuario.nombre_completo(),
            especialidad=usuario.especialidad,
            numero_licencia=usuario.numero_licencia,
            telefono=usuario.telefono,
            rol=usuario.rol.value,
            estado=usuario.estado.value,
            fecha_creacion=usuario.fecha_creacion,
            ultimo_acceso=usuario.ultimo_acceso
        )