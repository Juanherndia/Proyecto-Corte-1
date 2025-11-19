"""
Entidad Evento Médico - Domain Layer
Representa eventos médicos con jerarquía y polimorfismo.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from enum import Enum
from abc import ABC, abstractmethod


class TipoEvento(Enum):
    """Tipos de eventos médicos"""
    GUARDIA = "guardia"
    TURNO = "turno"
    EMERGENCIA = "emergencia"
    REUNION_CLINICA = "reunion_clinica"
    CIRUGIA = "cirugia"
    CONSULTA = "consulta"


class PrioridadEvento(Enum):
    """Prioridades de eventos médicos"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class EstadoEvento(Enum):
    """Estados de eventos médicos"""
    PROGRAMADO = "programado"
    EN_CURSO = "en_curso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"
    REPROGRAMADO = "reprogramado"


@dataclass
class EventoMedico(ABC):
    """
    Clase base abstracta para eventos médicos.
    Aplica OCP: Abierta para extensión, cerrada para modificación.
    """
    id: Optional[str]
    titulo: str
    descripcion: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    tipo: TipoEvento
    prioridad: PrioridadEvento
    estado: EstadoEvento
    usuario_id: str
    especialidad: Optional[str]
    ubicacion: Optional[str]
    notas: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones básicas de dominio"""
        if not self.titulo or len(self.titulo.strip()) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres")
        
        if not self.usuario_id:
            raise ValueError("Usuario ID es requerido")
        
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("Hora de fin debe ser posterior a hora de inicio")
    
    @abstractmethod
    def validar_reglas_negocio(self) -> List[str]:
        """Valida reglas de negocio específicas del tipo de evento"""
        pass
    
    @abstractmethod
    def calcular_duracion_minutos(self) -> int:
        """Calcula la duración del evento en minutos"""
        pass
    
    def es_evento_critico(self) -> bool:
        """Determina si el evento es crítico"""
        return self.prioridad == PrioridadEvento.CRITICA
    
    def puede_ser_cancelado(self) -> bool:
        """Determina si el evento puede ser cancelado"""
        return self.estado in [EstadoEvento.PROGRAMADO, EstadoEvento.REPROGRAMADO]
    
    def iniciar_evento(self):
        """Inicia el evento"""
        if self.estado != EstadoEvento.PROGRAMADO:
            raise ValueError("Solo eventos programados pueden iniciarse")
        self.estado = EstadoEvento.EN_CURSO
        self.fecha_actualizacion = datetime.now()
    
    def completar_evento(self):
        """Completa el evento"""
        if self.estado != EstadoEvento.EN_CURSO:
            raise ValueError("Solo eventos en curso pueden completarse")
        self.estado = EstadoEvento.COMPLETADO
        self.fecha_actualizacion = datetime.now()
    
    def cancelar_evento(self, motivo: str):
        """Cancela el evento"""
        if not self.puede_ser_cancelado():
            raise ValueError("Este evento no puede ser cancelado")
        self.estado = EstadoEvento.CANCELADO
        self.notas = f"Cancelado: {motivo}"
        self.fecha_actualizacion = datetime.now()


@dataclass
class Guardia(EventoMedico):
    """
    Entidad específica para guardias médicas.
    Implementa LSP: Puede sustituir a EventoMedico sin alterar funcionalidad.
    """
    turno: str  # "mañana", "tarde", "noche"
    es_fin_semana: bool = False
    requiere_supervisor: bool = False
    
    def validar_reglas_negocio(self) -> List[str]:
        """Validaciones específicas para guardias"""
        errores = []
        
        # Una guardia debe durar al menos 8 horas
        if self.calcular_duracion_minutos() < 480:
            errores.append("Una guardia debe durar al menos 8 horas")
        
        # Guardias nocturnas requieren supervisor si es residente
        if self.turno == "noche" and not self.requiere_supervisor:
            errores.append("Guardias nocturnas requieren supervisor")
        
        return errores
    
    def calcular_duracion_minutos(self) -> int:
        """Calcula duración de la guardia"""
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        fin = datetime.combine(self.fecha, self.hora_fin)
        
        # Si la hora de fin es menor, asumimos que termina al día siguiente
        if self.hora_fin < self.hora_inicio:
            fin = fin.replace(day=fin.day + 1)
        
        return int((fin - inicio).total_seconds() / 60)


@dataclass
class Emergencia(EventoMedico):
    """
    Entidad específica para emergencias médicas.
    """
    codigo_emergencia: str
    paciente_info: Optional[Dict[str, Any]] = None
    equipo_medico: Optional[List[str]] = None
    recursos_necesarios: Optional[List[str]] = None
    
    def validar_reglas_negocio(self) -> List[str]:
        """Validaciones específicas para emergencias"""
        errores = []
        
        # Las emergencias deben ser críticas o altas
        if self.prioridad not in [PrioridadEvento.CRITICA, PrioridadEvento.ALTA]:
            errores.append("Las emergencias deben tener prioridad alta o crítica")
        
        # Debe tener código de emergencia
        if not self.codigo_emergencia:
            errores.append("Código de emergencia es requerido")
        
        return errores
    
    def calcular_duracion_minutos(self) -> int:
        """Las emergencias tienen duración variable"""
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        fin = datetime.combine(self.fecha, self.hora_fin)
        return int((fin - inicio).total_seconds() / 60)
    
    def asignar_equipo_medico(self, equipo: List[str]):
        """Asigna equipo médico a la emergencia"""
        self.equipo_medico = equipo
        self.fecha_actualizacion = datetime.now()


@dataclass
class ReunionClinica(EventoMedico):
    """
    Entidad específica para reuniones clínicas.
    """
    tema_principal: str
    participantes: List[str]
    casos_revisar: Optional[List[str]] = None
    requiere_presentacion: bool = False
    
    def validar_reglas_negocio(self) -> List[str]:
        """Validaciones específicas para reuniones clínicas"""
        errores = []
        
        # Debe tener al menos 2 participantes
        if len(self.participantes) < 2:
            errores.append("Una reunión clínica debe tener al menos 2 participantes")
        
        # No debe exceder 4 horas
        if self.calcular_duracion_minutos() > 240:
            errores.append("Una reunión clínica no debe exceder 4 horas")
        
        return errores
    
    def calcular_duracion_minutos(self) -> int:
        """Calcula duración de la reunión"""
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        fin = datetime.combine(self.fecha, self.hora_fin)
        return int((fin - inicio).total_seconds() / 60)
    
    def agregar_participante(self, usuario_id: str):
        """Agrega un participante a la reunión"""
        if usuario_id not in self.participantes:
            self.participantes.append(usuario_id)
            self.fecha_actualizacion = datetime.now()