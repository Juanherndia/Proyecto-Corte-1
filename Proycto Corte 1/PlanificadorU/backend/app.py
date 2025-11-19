"""
Aplicación principal Flask con Clean Architecture.
Implementa el patrón de arquitectura limpia y principios SOLID.
"""
import asyncio
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from config.settings import load_config
from config.di_container import DIContainer
from src.interfaces.api.middleware.auth_middleware import CORSMiddleware


def create_app() -> Flask:
    """
    Factory para crear la aplicación Flask.
    Aplica el patrón Factory Method.
    """
    # Cargar configuración
    config = load_config()
    
    # Crear aplicación Flask
    app = Flask(__name__)
    app.config['DEBUG'] = config.debug
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configurar CORS
    CORS(app, origins=config.security.cors_allowed_origins)
    
    # Crear contenedor de dependencias
    di_container = DIContainer(config)
    
    # Configurar middleware CORS personalizado
    cors_middleware = CORSMiddleware(
        allowed_origins=config.security.cors_allowed_origins,
        allowed_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        allowed_headers=['Content-Type', 'Authorization']
    )
    
    @app.after_request
    def after_request(response):
        return cors_middleware.apply_cors_headers(response)
    
    # Registrar blueprints (controladores)
    usuario_controller = di_container.get_service('usuario_controller')
    app.register_blueprint(usuario_controller.blueprint)
    
    # Rutas de salud y información
    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint de verificación de salud"""
        return jsonify({
            'status': 'healthy',
            'service': 'Planificador Médico API',
            'version': '1.0.0',
            'environment': config.environment
        }), 200
    
    @app.route('/api/info', methods=['GET'])
    def api_info():
        """Información de la API"""
        return jsonify({
            'name': 'Planificador Médico API',
            'version': '1.0.0',
            'description': 'Sistema de gestión médica y emergencias',
            'environment': config.environment,
            'features': [
                'Gestión de usuarios médicos',
                'Autenticación JWT',
                'Autorización basada en roles',
                'Clean Architecture',
                'Principios SOLID'
            ],
            'endpoints': {
                'auth': '/api/usuarios/login',
                'register': '/api/usuarios/register',
                'users': '/api/usuarios',
                'profile': '/api/usuarios/me',
                'health': '/health'
            }
        }), 200
    
    # Manejo de errores globales
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Recurso no encontrado',
            'code': 'NOT_FOUND',
            'message': 'La ruta solicitada no existe'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Método no permitido',
            'code': 'METHOD_NOT_ALLOWED',
            'message': 'El método HTTP no está permitido para esta ruta'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f"Error interno: {str(error)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'code': 'INTERNAL_SERVER_ERROR',
            'message': 'Ha ocurrido un error inesperado'
        }), 500
    
    # Middleware para logging de requests
    @app.before_request
    def log_request():
        if config.debug:
            logging.info(f"{request.method} {request.url} - {request.remote_addr}")
    
    return app


def run_development_server():
    """
    Ejecuta el servidor de desarrollo.
    """
    config = load_config()
    app = create_app()
    
    print(f"""
    🏥 Planificador Médico API
    
    Servidor iniciando en: http://{config.host}:{config.port}
    Ambiente: {config.environment}
    Debug: {config.debug}
    
    Endpoints disponibles:
    - GET  /health                    - Estado del servicio
    - GET  /api/info                  - Información de la API
    - POST /api/usuarios/register     - Registro de usuarios
    - POST /api/usuarios/login        - Login de usuarios
    - GET  /api/usuarios              - Lista de usuarios (requiere auth)
    - GET  /api/usuarios/me           - Perfil del usuario (requiere auth)
    - GET  /api/usuarios/<id>         - Usuario específico (requiere auth)
    - PUT  /api/usuarios/<id>         - Actualizar usuario (requiere auth)
    
    Para detener el servidor: Ctrl+C
    """)
    
    try:
        app.run(
            host=config.host,
            port=config.port,
            debug=config.debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")


if __name__ == '__main__':
    run_development_server()
