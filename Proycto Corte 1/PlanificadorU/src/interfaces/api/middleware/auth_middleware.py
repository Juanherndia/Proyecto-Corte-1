"""
Middleware de autenticación y autorización - Interface Layer
Protege las rutas de la API y maneja la seguridad.
"""
from functools import wraps
from flask import request, jsonify, g
from typing import List, Optional, Callable
from ...infrastructure.security.jwt_service import IJWTService
from ...application.use_cases.usuario_use_cases import ObtenerUsuarioPorIdUseCase


class AuthMiddleware:
    """
    Middleware para autenticación y autorización.
    Aplica SRP: Solo maneja aspectos de seguridad.
    """
    
    def __init__(self, 
                 jwt_service: IJWTService,
                 obtener_usuario_use_case: ObtenerUsuarioPorIdUseCase):
        self._jwt_service = jwt_service
        self._obtener_usuario_use_case = obtener_usuario_use_case
    
    def require_auth(self, func: Callable) -> Callable:
        """
        Decorador que requiere autenticación válida.
        
        Args:
            func: Función a proteger
            
        Returns:
            Función decorada con verificación de autenticación
        """
        @wraps(func)
        async def decorated_function(*args, **kwargs):
            try:
                # Extraer token del header Authorization
                auth_header = request.headers.get('Authorization')
                if not auth_header:
                    return jsonify({
                        'error': 'Token de autenticación requerido',
                        'code': 'AUTH_REQUIRED'
                    }), 401
                
                # Validar formato del header
                if not auth_header.startswith('Bearer '):
                    return jsonify({
                        'error': 'Formato de token inválido',
                        'code': 'INVALID_TOKEN_FORMAT'
                    }), 401
                
                # Extraer y validar token
                token = auth_header.split(' ')[1]
                payload = self._jwt_service.validate_token(token)
                
                if not payload:
                    return jsonify({
                        'error': 'Token inválido o expirado',
                        'code': 'INVALID_TOKEN'
                    }), 401
                
                # Obtener información del usuario
                user_id = payload.get('user_id')
                if not user_id:
                    return jsonify({
                        'error': 'Token malformado',
                        'code': 'MALFORMED_TOKEN'
                    }), 401
                
                # Verificar que el usuario existe y está activo
                try:
                    usuario = await self._obtener_usuario_use_case.execute(user_id)
                    if usuario.estado != 'activo':
                        return jsonify({
                            'error': 'Usuario inactivo',
                            'code': 'USER_INACTIVE'
                        }), 401
                    
                    # Almacenar información del usuario en el contexto
                    g.current_user = usuario
                    g.token_payload = payload
                    
                except ValueError:
                    return jsonify({
                        'error': 'Usuario no encontrado',
                        'code': 'USER_NOT_FOUND'
                    }), 401
                
                return await func(*args, **kwargs)
                
            except Exception as e:
                return jsonify({
                    'error': 'Error de autenticación',
                    'code': 'AUTH_ERROR',
                    'details': str(e)
                }), 500
        
        return decorated_function
    
    def require_roles(self, roles: List[str]) -> Callable:
        """
        Decorador que requiere roles específicos.
        
        Args:
            roles: Lista de roles permitidos
            
        Returns:
            Decorador de función
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def decorated_function(*args, **kwargs):
                # Verificar que el usuario está autenticado
                if not hasattr(g, 'current_user'):
                    return jsonify({
                        'error': 'Autenticación requerida',
                        'code': 'AUTH_REQUIRED'
                    }), 401
                
                # Verificar rol del usuario
                user_role = g.current_user.rol
                if user_role not in roles:
                    return jsonify({
                        'error': 'Permisos insuficientes',
                        'code': 'INSUFFICIENT_PERMISSIONS',
                        'required_roles': roles,
                        'user_role': user_role
                    }), 403
                
                return await func(*args, **kwargs)
            
            return decorated_function
        return decorator
    
    def require_medical_staff(self, func: Callable) -> Callable:
        """
        Decorador que requiere ser personal médico.
        
        Args:
            func: Función a proteger
            
        Returns:
            Función decorada con verificación de personal médico
        """
        return self.require_roles(['medico', 'residente', 'enfermero'])(func)
    
    def require_admin(self, func: Callable) -> Callable:
        """
        Decorador que requiere ser administrador.
        
        Args:
            func: Función a proteger
            
        Returns:
            Función decorada con verificación de administrador
        """
        return self.require_roles(['administrador'])(func)
    
    def require_emergency_access(self, func: Callable) -> Callable:
        """
        Decorador que requiere acceso a emergencias.
        
        Args:
            func: Función a proteger
            
        Returns:
            Función decorada con verificación de acceso a emergencias
        """
        @wraps(func)
        async def decorated_function(*args, **kwargs):
            # Verificar autenticación
            if not hasattr(g, 'current_user'):
                return jsonify({
                    'error': 'Autenticación requerida',
                    'code': 'AUTH_REQUIRED'
                }), 401
            
            # Verificar permisos para emergencias
            user_role = g.current_user.rol
            if user_role not in ['medico', 'administrador']:
                return jsonify({
                    'error': 'Sin acceso a emergencias',
                    'code': 'NO_EMERGENCY_ACCESS'
                }), 403
            
            return await func(*args, **kwargs)
        
        return decorated_function
    
    def optional_auth(self, func: Callable) -> Callable:
        """
        Decorador para autenticación opcional.
        Carga información del usuario si el token está presente.
        
        Args:
            func: Función a decorar
            
        Returns:
            Función decorada con autenticación opcional
        """
        @wraps(func)
        async def decorated_function(*args, **kwargs):
            try:
                auth_header = request.headers.get('Authorization')
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    payload = self._jwt_service.validate_token(token)
                    
                    if payload:
                        user_id = payload.get('user_id')
                        if user_id:
                            try:
                                usuario = await self._obtener_usuario_use_case.execute(user_id)
                                g.current_user = usuario
                                g.token_payload = payload
                            except ValueError:
                                pass  # Usuario no encontrado, continuar sin autenticación
                
                return await func(*args, **kwargs)
                
            except Exception:
                # En caso de error, continuar sin autenticación
                return await func(*args, **kwargs)
        
        return decorated_function


class CORSMiddleware:
    """
    Middleware para manejo de CORS.
    """
    
    def __init__(self, 
                 allowed_origins: List[str] = None,
                 allowed_methods: List[str] = None,
                 allowed_headers: List[str] = None):
        self.allowed_origins = allowed_origins or ['*']
        self.allowed_methods = allowed_methods or ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
        self.allowed_headers = allowed_headers or ['Content-Type', 'Authorization']
    
    def apply_cors_headers(self, response):
        """Aplica headers CORS a la respuesta"""
        response.headers['Access-Control-Allow-Origin'] = ', '.join(self.allowed_origins)
        response.headers['Access-Control-Allow-Methods'] = ', '.join(self.allowed_methods)
        response.headers['Access-Control-Allow-Headers'] = ', '.join(self.allowed_headers)
        response.headers['Access-Control-Max-Age'] = '3600'
        return response