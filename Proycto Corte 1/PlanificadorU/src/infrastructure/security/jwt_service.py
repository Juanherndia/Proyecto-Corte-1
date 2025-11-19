"""
Servicio JWT para autenticación - Infrastructure Layer
Maneja la generación y validación de tokens JWT.
"""
from abc import ABC, abstractmethod
import jwt
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional


class IJWTService(ABC):
    """Interfaz para el servicio JWT"""
    
    @abstractmethod
    def generate_token(self, payload: Dict[str, Any]) -> Tuple[str, datetime]:
        """Genera un token JWT"""
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Valida y decodifica un token JWT"""
        pass
    
    @abstractmethod
    def refresh_token(self, token: str) -> Tuple[str, datetime]:
        """Renueva un token JWT"""
        pass


class JWTService(IJWTService):
    """
    Implementación del servicio JWT.
    Aplica SRP: Solo maneja operaciones JWT.
    """
    
    def __init__(self, 
                 secret_key: str = None,
                 algorithm: str = "HS256",
                 expiration_hours: int = 24):
        """
        Inicializa el servicio JWT.
        
        Args:
            secret_key: Clave secreta para firmar tokens
            algorithm: Algoritmo de cifrado
            expiration_hours: Horas de expiración del token
        """
        self._secret_key = secret_key or os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
        self._algorithm = algorithm
        self._expiration_hours = expiration_hours
        
        # Validar configuración
        if not self._secret_key or len(self._secret_key) < 32:
            raise ValueError("La clave secreta JWT debe tener al menos 32 caracteres")
    
    def generate_token(self, payload: Dict[str, Any]) -> Tuple[str, datetime]:
        """
        Genera un nuevo token JWT.
        
        Args:
            payload: Datos a incluir en el token
            
        Returns:
            Tupla con (token, fecha_expiracion)
        """
        now = datetime.utcnow()
        expiration = now + timedelta(hours=self._expiration_hours)
        
        # Payload completo con metadatos
        full_payload = {
            **payload,
            "iat": now,  # Issued at
            "exp": expiration,  # Expiration
            "iss": "planificador-medico",  # Issuer
        }
        
        # Generar token
        token = jwt.encode(
            full_payload,
            self._secret_key,
            algorithm=self._algorithm
        )
        
        return token, expiration
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida y decodifica un token JWT.
        
        Args:
            token: Token JWT a validar
            
        Returns:
            Payload decodificado o None si es inválido
        """
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm]
            )
            
            # Verificar que el token no haya expirado
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception:
            return None
    
    def refresh_token(self, token: str) -> Tuple[str, datetime]:
        """
        Renueva un token JWT existente.
        
        Args:
            token: Token actual a renovar
            
        Returns:
            Tupla con (nuevo_token, nueva_fecha_expiracion)
            
        Raises:
            ValueError: Si el token es inválido o expirado
        """
        payload = self.validate_token(token)
        if not payload:
            raise ValueError("Token inválido o expirado")
        
        # Remover metadatos temporales para regenerar
        user_data = {
            key: value for key, value in payload.items()
            if key not in ["iat", "exp", "iss"]
        }
        
        return self.generate_token(user_data)
    
    def extract_user_id(self, token: str) -> Optional[str]:
        """
        Extrae el ID de usuario de un token.
        
        Args:
            token: Token JWT
            
        Returns:
            ID de usuario o None si no es válido
        """
        payload = self.validate_token(token)
        return payload.get("user_id") if payload else None
    
    def extract_user_role(self, token: str) -> Optional[str]:
        """
        Extrae el rol de usuario de un token.
        
        Args:
            token: Token JWT
            
        Returns:
            Rol de usuario o None si no es válido
        """
        payload = self.validate_token(token)
        return payload.get("rol") if payload else None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Verifica si un token ha expirado.
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            True si el token ha expirado
        """
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                options={"verify_exp": False}  # No verificar expiración para obtener payload
            )
            
            exp = payload.get("exp")
            if not exp:
                return True
            
            return datetime.utcnow() > datetime.fromtimestamp(exp)
            
        except Exception:
            return True