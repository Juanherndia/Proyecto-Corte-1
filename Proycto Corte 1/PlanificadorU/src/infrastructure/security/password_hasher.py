"""
Servicio de hash de contraseñas - Infrastructure Layer
Implementa el cifrado de contraseñas usando bcrypt.
Cumple con DIP: Implementa interfaz definida en el dominio.
"""
from abc import ABC, abstractmethod
import bcrypt
from typing import Union


class IPasswordHasher(ABC):
    """Interfaz para el servicio de hash de contraseñas"""
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Genera hash de una contraseña"""
        pass
    
    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica una contraseña contra su hash"""
        pass


class BCryptPasswordHasher(IPasswordHasher):
    """
    Implementación concreta usando BCrypt.
    Aplica SRP: Solo se encarga del hashing de contraseñas.
    """
    
    def __init__(self, rounds: int = 12):
        """
        Inicializa el hasher con el número de rondas.
        
        Args:
            rounds: Número de rondas para el algoritmo bcrypt (recomendado: 10-12)
        """
        self._rounds = rounds
    
    def hash_password(self, password: str) -> str:
        """
        Genera un hash seguro de la contraseña.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña en formato string
            
        Raises:
            ValueError: Si la contraseña está vacía
        """
        if not password or not password.strip():
            raise ValueError("La contraseña no puede estar vacía")
        
        # Validar longitud mínima
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        
        # Convertir a bytes y generar hash
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=self._rounds)
        password_hash = bcrypt.hashpw(password_bytes, salt)
        
        return password_hash.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash.
        
        Args:
            password: Contraseña en texto plano
            password_hash: Hash almacenado de la contraseña
            
        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        if not password or not password_hash:
            return False
        
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            return False
    
    def is_password_strong(self, password: str) -> tuple[bool, list[str]]:
        """
        Verifica si una contraseña cumple con los criterios de seguridad.
        
        Args:
            password: Contraseña a validar
            
        Returns:
            Tupla con (es_fuerte: bool, errores: list[str])
        """
        errors = []
        
        # Longitud mínima
        if len(password) < 8:
            errors.append("Debe tener al menos 8 caracteres")
        
        # Al menos una letra minúscula
        if not any(c.islower() for c in password):
            errors.append("Debe contener al menos una letra minúscula")
        
        # Al menos una letra mayúscula
        if not any(c.isupper() for c in password):
            errors.append("Debe contener al menos una letra mayúscula")
        
        # Al menos un dígito
        if not any(c.isdigit() for c in password):
            errors.append("Debe contener al menos un número")
        
        # Al menos un carácter especial
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            errors.append("Debe contener al menos un carácter especial")
        
        # No debe contener espacios
        if ' ' in password:
            errors.append("No debe contener espacios")
        
        return len(errors) == 0, errors