"""
Repositorio de Eventos Médicos - Domain Layer Interface
Define el contrato para la persistencia de eventos médicos.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date, datetime
from ..entities.evento_medico import EventoMedico, TipoEvento, PrioridadEvento, EstadoEvento


class IEventoMedicoRepository(ABC):
    """
    Interfaz del repositorio de eventos médicos.
    Cumple con ISP: Métodos específicos para eventos médicos.
    """
    
    @abstractmethod
    async def crear(self, evento: EventoMedico) -> EventoMedico:
        """Crea un nuevo evento médico"""
        pass
    
    @abstractmethod
    async def buscar_por_id(self, id: str) -> Optional[EventoMedico]:
        """Busca un evento por ID"""
        pass
    
    @abstractmethod
    async def actualizar(self, evento: EventoMedico) -> EventoMedico:
        """Actualiza un evento existente"""
        pass
    
    @abstractmethod
    async def eliminar(self, id: str) -> bool:
        """Elimina un evento por ID"""
        pass
    
    @abstractmethod
    async def listar_por_usuario(self, usuario_id: str) -> List[EventoMedico]:
        """Lista eventos de un usuario específico"""
        pass
    
    @abstractmethod
    async def listar_por_fecha(self, fecha: date) -> List[EventoMedico]:
        """Lista eventos de una fecha específica"""
        pass
    
    @abstractmethod
    async def listar_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date) -> List[EventoMedico]:
        """Lista eventos en un rango de fechas"""
        pass
    
    @abstractmethod
    async def listar_por_tipo(self, tipo: TipoEvento) -> List[EventoMedico]:
        """Lista eventos por tipo"""
        pass
    
    @abstractmethod
    async def listar_por_prioridad(self, prioridad: PrioridadEvento) -> List[EventoMedico]:
        """Lista eventos por prioridad"""
        pass
    
    @abstractmethod
    async def listar_por_estado(self, estado: EstadoEvento) -> List[EventoMedico]:
        """Lista eventos por estado"""
        pass
    
    @abstractmethod
    async def listar_emergencias_activas(self) -> List[EventoMedico]:
        """Lista emergencias activas (en curso o programadas)"""
        pass
    
    @abstractmethod
    async def listar_guardias_por_turno(self, turno: str, fecha: date) -> List[EventoMedico]:
        """Lista guardias por turno en una fecha específica"""
        pass
    
    @abstractmethod
    async def verificar_conflicto_horario(self, usuario_id: str, fecha: date, 
                                        hora_inicio: datetime, hora_fin: datetime,
                                        excluir_evento_id: Optional[str] = None) -> bool:
        """Verifica si existe conflicto de horario para un usuario"""
        pass
    
    @abstractmethod
    async def contar_eventos_por_usuario_fecha(self, usuario_id: str, fecha: date) -> int:
        """Cuenta eventos de un usuario en una fecha específica"""
        pass