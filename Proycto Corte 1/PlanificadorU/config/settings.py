"""
Configuración de la aplicación.
Centraliza todas las configuraciones del sistema.
"""
import os
from dataclasses import dataclass
from typing import List


@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    host: str = "localhost"
    port: int = 5432
    name: str = "planificador_medico"
    username: str = "postgres"
    password: str = ""
    
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class SecurityConfig:
    """Configuración de seguridad"""
    jwt_secret_key: str = "dev-secret-key-change-in-production"
    jwt_expiration_hours: int = 24
    password_hash_rounds: int = 12
    cors_allowed_origins: List[str] = None
    
    def __post_init__(self):
        if self.cors_allowed_origins is None:
            self.cors_allowed_origins = ["http://localhost:3000", "http://localhost:8080"]


@dataclass
class AppConfig:
    """Configuración principal de la aplicación"""
    environment: str = "development"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 5000
    log_level: str = "INFO"
    
    # Configuraciones específicas
    database: DatabaseConfig = None
    security: SecurityConfig = None
    
    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig()
        if self.security is None:
            self.security = SecurityConfig()


def load_config() -> AppConfig:
    """
    Carga la configuración desde variables de entorno.
    
    Returns:
        AppConfig: Configuración de la aplicación
    """
    # Configuración de base de datos
    db_config = DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        name=os.getenv("DB_NAME", "planificador_medico"),
        username=os.getenv("DB_USERNAME", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )
    
    # Configuración de seguridad
    security_config = SecurityConfig(
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production"),
        jwt_expiration_hours=int(os.getenv("JWT_EXPIRATION_HOURS", "24")),
        password_hash_rounds=int(os.getenv("PASSWORD_HASH_ROUNDS", "12")),
        cors_allowed_origins=os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
    )
    
    # Configuración principal
    app_config = AppConfig(
        environment=os.getenv("ENVIRONMENT", "development"),
        debug=os.getenv("DEBUG", "true").lower() == "true",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        database=db_config,
        security=security_config
    )
    
    return app_config


# Configuración global
config = load_config()