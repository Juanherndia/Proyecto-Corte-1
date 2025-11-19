"""
Data Transfer Objects para la aplicación.
DTOs para separar la lógica de presentación del dominio.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import date, time, datetime


@dataclass
class CrearUsuarioDTO:
    """DTO para crear un nuevo usuario"""
    email: str
    nombre: str
    apellido: str
    especialidad: Optional[str]
    numero_licencia: str
    telefono: str
    rol: str
    password: str


@dataclass
class ActualizarUsuarioDTO:
    """DTO para actualizar un usuario existente"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    estado: Optional[str] = None


@dataclass
class UsuarioResponseDTO:
    """DTO de respuesta para usuarios"""
    id: str
    email: str
    nombre: str
    apellido: str
    nombre_completo: str
    especialidad: Optional[str]
    numero_licencia: str
    telefono: str
    rol: str
    estado: str
    fecha_creacion: datetime
    ultimo_acceso: Optional[datetime]


@dataclass
class LoginDTO:
    """DTO para login de usuario"""
    email: str
    password: str


@dataclass
class LoginResponseDTO:
    """DTO de respuesta para login"""
    usuario: UsuarioResponseDTO
    token: str
    expires_at: datetime


@dataclass
class CrearEventoMedicoDTO:
    """DTO para crear un evento médico"""
    titulo: str
    descripcion: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    tipo: str
    especialidad: Optional[str] = None
    ubicacion: Optional[str] = None
    notas: Optional[str] = None
    # Campos específicos según el tipo
    datos_especificos: Optional[Dict[str, Any]] = None


@dataclass
class ActualizarEventoMedicoDTO:
    """DTO para actualizar un evento médico"""
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    especialidad: Optional[str] = None
    ubicacion: Optional[str] = None
    notas: Optional[str] = None
    estado: Optional[str] = None


@dataclass
class EventoMedicoResponseDTO:
    """DTO de respuesta para eventos médicos"""
    id: str
    titulo: str
    descripcion: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    tipo: str
    prioridad: str
    estado: str
    especialidad: Optional[str]
    ubicacion: Optional[str]
    notas: Optional[str]
    duracion_minutos: int
    usuario_id: str
    medico_nombre: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    # Campos específicos según el tipo
    datos_especificos: Optional[Dict[str, Any]] = None


@dataclass
class CalendarioRequestDTO:
    """DTO para solicitud de calendario"""
    usuario_id: Optional[str] = None
    fecha_inicio: date
    fecha_fin: date
    tipos_evento: Optional[List[str]] = None
    especialidades: Optional[List[str]] = None


@dataclass
class CalendarioResponseDTO:
    """DTO de respuesta para calendario"""
    eventos: List[EventoMedicoResponseDTO]
    estadisticas: Dict[str, Any]
    filtros_aplicados: Dict[str, Any]


@dataclass
class ReportarEmergenciaDTO:
    """DTO para reportar emergencia"""
    titulo: str
    descripcion: str
    codigo_emergencia: str
    ubicacion: str
    prioridad: str = "critica"
    paciente_info: Optional[Dict[str, Any]] = None
    recursos_necesarios: Optional[List[str]] = None


@dataclass
class GuardiaDTO:
    """DTO específico para guardias"""
    titulo: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    turno: str
    especialidad: str
    ubicacion: str
    es_fin_semana: bool = False
    requiere_supervisor: bool = False
    descripcion: str = ""


@dataclass
class DisponibilidadMedicoDTO:
    """DTO para verificar disponibilidad de médico"""
    usuario_id: str
    fecha: date
    hora_inicio: time
    hora_fin: time


@dataclass
class EstadisticasDTO:
    """DTO para estadísticas del sistema"""
    total_usuarios: int
    usuarios_activos: int
    medicos_de_guardia: int
    emergencias_activas: int
    eventos_hoy: int
    eventos_semana: int
    guardias_programadas: int