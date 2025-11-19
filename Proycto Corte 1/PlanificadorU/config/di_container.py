"""
Inyección de dependencias - Dependency Injection Container
Configura y maneja todas las dependencias de la aplicación.
Aplica DIP: Invierte las dependencias y centraliza la configuración.
"""
from typing import Dict, Any
from config.settings import AppConfig
from src.domain.repositories.usuario_repository import IUsuarioRepository
from src.infrastructure.repositories.in_memory_usuario_repository import InMemoryUsuarioRepository
from src.infrastructure.security.password_hasher import IPasswordHasher, BCryptPasswordHasher
from src.infrastructure.security.jwt_service import IJWTService, JWTService
from src.application.use_cases.usuario_use_cases import (
    CrearUsuarioUseCase, LoginUsuarioUseCase, ActualizarUsuarioUseCase,
    ListarUsuariosUseCase, ObtenerUsuarioPorIdUseCase
)
from src.interfaces.api.middleware.auth_middleware import AuthMiddleware
from src.interfaces.api.controllers.usuario_controller import UsuarioController


class DIContainer:
    """
    Contenedor de inyección de dependencias.
    Implementa el patrón Service Locator y Factory.
    """
    
    def __init__(self, config: AppConfig):
        self._config = config
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
        self._setup_services()
    
    def _setup_services(self):
        """Configura todos los servicios y sus dependencias"""
        
        # Repositories (Singletons)
        self._register_singleton('usuario_repository', self._create_usuario_repository)
        
        # Security Services (Singletons)
        self._register_singleton('password_hasher', self._create_password_hasher)
        self._register_singleton('jwt_service', self._create_jwt_service)
        
        # Use Cases (Transient - nueva instancia cada vez)
        self._register_transient('crear_usuario_use_case', self._create_crear_usuario_use_case)
        self._register_transient('login_usuario_use_case', self._create_login_usuario_use_case)
        self._register_transient('actualizar_usuario_use_case', self._create_actualizar_usuario_use_case)
        self._register_transient('listar_usuarios_use_case', self._create_listar_usuarios_use_case)
        self._register_transient('obtener_usuario_use_case', self._create_obtener_usuario_use_case)
        
        # Middleware (Singletons)
        self._register_singleton('auth_middleware', self._create_auth_middleware)
        
        # Controllers (Singletons)
        self._register_singleton('usuario_controller', self._create_usuario_controller)
    
    def _register_singleton(self, name: str, factory_func):
        """Registra un servicio como singleton"""
        self._services[name] = ('singleton', factory_func)
    
    def _register_transient(self, name: str, factory_func):
        """Registra un servicio como transient"""
        self._services[name] = ('transient', factory_func)
    
    def get_service(self, name: str):
        """Obtiene un servicio por nombre"""
        if name not in self._services:
            raise ValueError(f"Servicio '{name}' no encontrado")
        
        lifecycle, factory_func = self._services[name]
        
        if lifecycle == 'singleton':
            if name not in self._singletons:
                self._singletons[name] = factory_func()
            return self._singletons[name]
        else:  # transient
            return factory_func()
    
    # Factory methods para crear servicios
    
    def _create_usuario_repository(self) -> IUsuarioRepository:
        """Crea el repositorio de usuarios"""
        repository = InMemoryUsuarioRepository()
        # Inicializar con datos de prueba en desarrollo
        if self._config.environment == "development":
            import asyncio
            asyncio.create_task(repository.inicializar_datos_prueba())
        return repository
    
    def _create_password_hasher(self) -> IPasswordHasher:
        """Crea el servicio de hash de contraseñas"""
        return BCryptPasswordHasher(rounds=self._config.security.password_hash_rounds)
    
    def _create_jwt_service(self) -> IJWTService:
        """Crea el servicio JWT"""
        return JWTService(
            secret_key=self._config.security.jwt_secret_key,
            expiration_hours=self._config.security.jwt_expiration_hours
        )
    
    def _create_crear_usuario_use_case(self) -> CrearUsuarioUseCase:
        """Crea el caso de uso para crear usuarios"""
        return CrearUsuarioUseCase(
            usuario_repository=self.get_service('usuario_repository'),
            password_hasher=self.get_service('password_hasher')
        )
    
    def _create_login_usuario_use_case(self) -> LoginUsuarioUseCase:
        """Crea el caso de uso para login"""
        return LoginUsuarioUseCase(
            usuario_repository=self.get_service('usuario_repository'),
            password_hasher=self.get_service('password_hasher'),
            jwt_service=self.get_service('jwt_service')
        )
    
    def _create_actualizar_usuario_use_case(self) -> ActualizarUsuarioUseCase:
        """Crea el caso de uso para actualizar usuarios"""
        return ActualizarUsuarioUseCase(
            usuario_repository=self.get_service('usuario_repository')
        )
    
    def _create_listar_usuarios_use_case(self) -> ListarUsuariosUseCase:
        """Crea el caso de uso para listar usuarios"""
        return ListarUsuariosUseCase(
            usuario_repository=self.get_service('usuario_repository')
        )
    
    def _create_obtener_usuario_use_case(self) -> ObtenerUsuarioPorIdUseCase:
        """Crea el caso de uso para obtener usuario por ID"""
        return ObtenerUsuarioPorIdUseCase(
            usuario_repository=self.get_service('usuario_repository')
        )
    
    def _create_auth_middleware(self) -> AuthMiddleware:
        """Crea el middleware de autenticación"""
        return AuthMiddleware(
            jwt_service=self.get_service('jwt_service'),
            obtener_usuario_use_case=self.get_service('obtener_usuario_use_case')
        )
    
    def _create_usuario_controller(self) -> UsuarioController:
        """Crea el controlador de usuarios"""
        return UsuarioController(
            crear_usuario_use_case=self.get_service('crear_usuario_use_case'),
            login_usuario_use_case=self.get_service('login_usuario_use_case'),
            actualizar_usuario_use_case=self.get_service('actualizar_usuario_use_case'),
            listar_usuarios_use_case=self.get_service('listar_usuarios_use_case'),
            obtener_usuario_use_case=self.get_service('obtener_usuario_use_case'),
            auth_middleware=self.get_service('auth_middleware')
        )
    
    def get_config(self) -> AppConfig:
        """Obtiene la configuración de la aplicación"""
        return self._config