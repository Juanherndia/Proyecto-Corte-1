"""
Controlador de Usuarios - Interface Layer
Maneja las peticiones HTTP relacionadas con usuarios.
Cumple con SRP: Solo maneja la interfaz HTTP para usuarios.
"""
from flask import Blueprint, request, jsonify, g
from typing import Dict, Any
from ...middleware.auth_middleware import AuthMiddleware
from ....application.use_cases.usuario_use_cases import (
    CrearUsuarioUseCase, LoginUsuarioUseCase, ActualizarUsuarioUseCase,
    ListarUsuariosUseCase, ObtenerUsuarioPorIdUseCase
)
from ....application.dto.dtos import (
    CrearUsuarioDTO, LoginDTO, ActualizarUsuarioDTO
)


class UsuarioController:
    """
    Controlador REST para operaciones de usuarios.
    Aplica principios de Clean Architecture separando concerns.
    """
    
    def __init__(self,
                 crear_usuario_use_case: CrearUsuarioUseCase,
                 login_usuario_use_case: LoginUsuarioUseCase,
                 actualizar_usuario_use_case: ActualizarUsuarioUseCase,
                 listar_usuarios_use_case: ListarUsuariosUseCase,
                 obtener_usuario_use_case: ObtenerUsuarioPorIdUseCase,
                 auth_middleware: AuthMiddleware):
        
        self._crear_usuario_use_case = crear_usuario_use_case
        self._login_usuario_use_case = login_usuario_use_case
        self._actualizar_usuario_use_case = actualizar_usuario_use_case
        self._listar_usuarios_use_case = listar_usuarios_use_case
        self._obtener_usuario_use_case = obtener_usuario_use_case
        self._auth_middleware = auth_middleware
        
        # Crear blueprint
        self.blueprint = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')
        self._register_routes()
    
    def _register_routes(self):
        """Registra las rutas del controlador"""
        
        # Rutas públicas
        self.blueprint.add_url_rule(
            '/register', 
            'crear_usuario', 
            self.crear_usuario, 
            methods=['POST']
        )
        
        self.blueprint.add_url_rule(
            '/login', 
            'login', 
            self.login, 
            methods=['POST']
        )
        
        # Rutas protegidas
        self.blueprint.add_url_rule(
            '/', 
            'listar_usuarios',
            self._auth_middleware.require_auth(self.listar_usuarios),
            methods=['GET']
        )
        
        self.blueprint.add_url_rule(
            '/<string:usuario_id>', 
            'obtener_usuario',
            self._auth_middleware.require_auth(self.obtener_usuario),
            methods=['GET']
        )
        
        self.blueprint.add_url_rule(
            '/<string:usuario_id>', 
            'actualizar_usuario',
            self._auth_middleware.require_auth(self.actualizar_usuario),
            methods=['PUT']
        )
        
        self.blueprint.add_url_rule(
            '/me', 
            'obtener_perfil',
            self._auth_middleware.require_auth(self.obtener_perfil),
            methods=['GET']
        )
    
    async def crear_usuario(self) -> Dict[str, Any]:
        """
        Endpoint: POST /api/usuarios/register
        Crea un nuevo usuario en el sistema.
        """
        try:
            data = request.get_json()
            
            # Validar datos requeridos
            required_fields = ['email', 'nombre', 'apellido', 'numero_licencia', 
                             'telefono', 'rol', 'password']
            
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        'error': f'Campo requerido: {field}',
                        'code': 'MISSING_FIELD'
                    }), 400
            
            # Crear DTO
            dto = CrearUsuarioDTO(
                email=data['email'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                especialidad=data.get('especialidad'),
                numero_licencia=data['numero_licencia'],
                telefono=data['telefono'],
                rol=data['rol'],
                password=data['password']
            )
            
            # Ejecutar caso de uso
            usuario_creado = await self._crear_usuario_use_case.execute(dto)
            
            return jsonify({
                'message': 'Usuario creado exitosamente',
                'data': {
                    'id': usuario_creado.id,
                    'email': usuario_creado.email,
                    'nombre_completo': usuario_creado.nombre_completo,
                    'rol': usuario_creado.rol,
                    'estado': usuario_creado.estado,
                    'fecha_creacion': usuario_creado.fecha_creacion.isoformat()
                }
            }), 201
            
        except ValueError as e:
            return jsonify({
                'error': str(e),
                'code': 'VALIDATION_ERROR'
            }), 400
            
        except Exception as e:
            return jsonify({
                'error': 'Error interno del servidor',
                'code': 'INTERNAL_ERROR',
                'details': str(e)
            }), 500
    
    async def login(self) -> Dict[str, Any]:
        """
        Endpoint: POST /api/usuarios/login
        Autentica un usuario y retorna token JWT.
        """
        try:
            data = request.get_json()
            
            # Validar datos requeridos
            if not data.get('email') or not data.get('password'):
                return jsonify({
                    'error': 'Email y contraseña son requeridos',
                    'code': 'MISSING_CREDENTIALS'
                }), 400
            
            # Crear DTO
            dto = LoginDTO(
                email=data['email'],
                password=data['password']
            )
            
            # Ejecutar caso de uso
            login_result = await self._login_usuario_use_case.execute(dto)
            
            return jsonify({
                'message': 'Login exitoso',
                'data': {
                    'user': {
                        'id': login_result.usuario.id,
                        'email': login_result.usuario.email,
                        'nombre_completo': login_result.usuario.nombre_completo,
                        'rol': login_result.usuario.rol,
                        'especialidad': login_result.usuario.especialidad
                    },
                    'token': login_result.token,
                    'expires_at': login_result.expires_at.isoformat()
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'error': str(e),
                'code': 'AUTHENTICATION_ERROR'
            }), 401
            
        except Exception as e:
            return jsonify({
                'error': 'Error interno del servidor',
                'code': 'INTERNAL_ERROR',
                'details': str(e)
            }), 500
    
    async def listar_usuarios(self) -> Dict[str, Any]:
        """
        Endpoint: GET /api/usuarios
        Lista usuarios con filtros opcionales.
        """
        try:
            # Obtener parámetros de consulta
            rol = request.args.get('rol')
            estado = request.args.get('estado')
            especialidad = request.args.get('especialidad')
            
            # Ejecutar caso de uso
            usuarios = await self._listar_usuarios_use_case.execute(
                rol=rol,
                estado=estado,
                especialidad=especialidad
            )
            
            return jsonify({
                'message': 'Usuarios obtenidos exitosamente',
                'data': {
                    'usuarios': [
                        {
                            'id': u.id,
                            'email': u.email,
                            'nombre_completo': u.nombre_completo,
                            'especialidad': u.especialidad,
                            'rol': u.rol,
                            'estado': u.estado,
                            'ultimo_acceso': u.ultimo_acceso.isoformat() if u.ultimo_acceso else None
                        } for u in usuarios
                    ],
                    'total': len(usuarios),
                    'filtros': {
                        'rol': rol,
                        'estado': estado,
                        'especialidad': especialidad
                    }
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Error interno del servidor',
                'code': 'INTERNAL_ERROR',
                'details': str(e)
            }), 500
    
    async def obtener_usuario(self, usuario_id: str) -> Dict[str, Any]:
        """
        Endpoint: GET /api/usuarios/{id}
        Obtiene un usuario específico por ID.
        """
        try:
            # Verificar permisos: solo admin o el mismo usuario
            current_user = g.current_user
            if current_user.rol != 'administrador' and current_user.id != usuario_id:
                return jsonify({
                    'error': 'Sin permisos para ver este usuario',
                    'code': 'INSUFFICIENT_PERMISSIONS'
                }), 403
            
            # Ejecutar caso de uso
            usuario = await self._obtener_usuario_use_case.execute(usuario_id)
            
            return jsonify({
                'message': 'Usuario obtenido exitosamente',
                'data': {
                    'id': usuario.id,
                    'email': usuario.email,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'nombre_completo': usuario.nombre_completo,
                    'especialidad': usuario.especialidad,
                    'numero_licencia': usuario.numero_licencia,
                    'telefono': usuario.telefono,
                    'rol': usuario.rol,
                    'estado': usuario.estado,
                    'fecha_creacion': usuario.fecha_creacion.isoformat(),
                    'ultimo_acceso': usuario.ultimo_acceso.isoformat() if usuario.ultimo_acceso else None
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'error': str(e),
                'code': 'USER_NOT_FOUND'
            }), 404
            
        except Exception as e:
            return jsonify({
                'error': 'Error interno del servidor',
                'code': 'INTERNAL_ERROR',
                'details': str(e)
            }), 500
    
    async def actualizar_usuario(self, usuario_id: str) -> Dict[str, Any]:
        """
        Endpoint: PUT /api/usuarios/{id}
        Actualiza los datos de un usuario.
        """
        try:
            # Verificar permisos
            current_user = g.current_user
            if current_user.rol != 'administrador' and current_user.id != usuario_id:
                return jsonify({
                    'error': 'Sin permisos para actualizar este usuario',
                    'code': 'INSUFFICIENT_PERMISSIONS'
                }), 403
            
            data = request.get_json()
            
            # Crear DTO
            dto = ActualizarUsuarioDTO(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                especialidad=data.get('especialidad'),
                telefono=data.get('telefono'),
                estado=data.get('estado') if current_user.rol == 'administrador' else None
            )
            
            # Ejecutar caso de uso
            usuario_actualizado = await self._actualizar_usuario_use_case.execute(usuario_id, dto)
            
            return jsonify({
                'message': 'Usuario actualizado exitosamente',
                'data': {
                    'id': usuario_actualizado.id,
                    'email': usuario_actualizado.email,
                    'nombre_completo': usuario_actualizado.nombre_completo,
                    'especialidad': usuario_actualizado.especialidad,
                    'telefono': usuario_actualizado.telefono,
                    'estado': usuario_actualizado.estado
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'error': str(e),
                'code': 'VALIDATION_ERROR'
            }), 400
            
        except Exception as e:
            return jsonify({
                'error': 'Error interno del servidor',
                'code': 'INTERNAL_ERROR',
                'details': str(e)
            }), 500
    
    async def obtener_perfil(self) -> Dict[str, Any]:
        """
        Endpoint: GET /api/usuarios/me
        Obtiene el perfil del usuario autenticado.
        """
        try:
            current_user = g.current_user
            
            return jsonify({
                'message': 'Perfil obtenido exitosamente',
                'data': {
                    'id': current_user.id,
                    'email': current_user.email,
                    'nombre': current_user.nombre,
                    'apellido': current_user.apellido,
                    'nombre_completo': current_user.nombre_completo,
                    'especialidad': current_user.especialidad,
                    'numero_licencia': current_user.numero_licencia,
                    'telefono': current_user.telefono,
                    'rol': current_user.rol,
                    'estado': current_user.estado,
                    'fecha_creacion': current_user.fecha_creacion.isoformat(),
                    'ultimo_acceso': current_user.ultimo_acceso.isoformat() if current_user.ultimo_acceso else None
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Error interno del servidor',
                'code': 'INTERNAL_ERROR',
                'details': str(e)
            }), 500