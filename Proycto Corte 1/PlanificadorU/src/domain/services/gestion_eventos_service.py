"""
Servicio de Dominio para gestión de eventos médicos.
Contiene lógica de negocio compleja que involucra múltiples entidades.
Cumple con SRP: Solo maneja lógica de coordinación de eventos médicos.
"""
from typing import List, Optional
from datetime import date, datetime, time, timedelta
from ..entities.evento_medico import EventoMedico, Guardia, Emergencia, TipoEvento, PrioridadEvento
from ..entities.usuario import Usuario, RolUsuario
from ..repositories.evento_medico_repository import IEventoMedicoRepository
from ..repositories.usuario_repository import IUsuarioRepository


class GestionEventosMedicosService:
    """
    Servicio de dominio para gestión de eventos médicos.
    Aplica principios SOLID y encapsula lógica de negocio compleja.
    """
    
    def __init__(self, 
                 evento_repository: IEventoMedicoRepository,
                 usuario_repository: IUsuarioRepository):
        self._evento_repository = evento_repository
        self._usuario_repository = usuario_repository
    
    async def programar_guardia(self, datos_guardia: dict, usuario_id: str) -> Guardia:
        """
        Programa una nueva guardia médica aplicando reglas de negocio.
        """
        # Verificar que el usuario existe y puede tener guardias
        usuario = await self._usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        if not usuario.es_medico():
            raise ValueError("Solo médicos pueden tener guardias asignadas")
        
        # Crear la guardia
        guardia = Guardia(
            id=None,
            titulo=datos_guardia["titulo"],
            descripcion=datos_guardia.get("descripcion", ""),
            fecha=datos_guardia["fecha"],
            hora_inicio=datos_guardia["hora_inicio"],
            hora_fin=datos_guardia["hora_fin"],
            tipo=TipoEvento.GUARDIA,
            prioridad=PrioridadEvento.ALTA,
            estado=datos_guardia.get("estado", "programado"),
            usuario_id=usuario_id,
            especialidad=datos_guardia.get("especialidad", usuario.especialidad),
            ubicacion=datos_guardia.get("ubicacion"),
            notas=datos_guardia.get("notas"),
            fecha_creacion=datetime.now(),
            turno=datos_guardia["turno"],
            es_fin_semana=datos_guardia.get("es_fin_semana", False),
            requiere_supervisor=datos_guardia.get("requiere_supervisor", False)
        )
        
        # Validar reglas de negocio específicas
        errores = guardia.validar_reglas_negocio()
        if errores:
            raise ValueError(f"Errores de validación: {', '.join(errores)}")
        
        # Verificar conflictos de horario
        tiene_conflicto = await self._evento_repository.verificar_conflicto_horario(
            usuario_id, guardia.fecha, 
            datetime.combine(guardia.fecha, guardia.hora_inicio),
            datetime.combine(guardia.fecha, guardia.hora_fin)
        )
        
        if tiene_conflicto:
            raise ValueError("Existe conflicto de horario con otro evento")
        
        # Verificar límites de guardias por semana
        await self._validar_limite_guardias_semanales(usuario_id, guardia.fecha)
        
        return await self._evento_repository.crear(guardia)
    
    async def reportar_emergencia(self, datos_emergencia: dict, reportado_por: str) -> Emergencia:
        """
        Reporta una nueva emergencia médica.
        """
        usuario = await self._usuario_repository.buscar_por_id(reportado_por)
        if not usuario:
            raise ValueError("Usuario reportante no encontrado")
        
        if not usuario.puede_gestionar_emergencias():
            raise ValueError("Usuario no autorizado para reportar emergencias")
        
        emergencia = Emergencia(
            id=None,
            titulo=datos_emergencia["titulo"],
            descripcion=datos_emergencia["descripcion"],
            fecha=datos_emergencia.get("fecha", date.today()),
            hora_inicio=datos_emergencia.get("hora_inicio", datetime.now().time()),
            hora_fin=datos_emergencia["hora_fin"],
            tipo=TipoEvento.EMERGENCIA,
            prioridad=PrioridadEvento.CRITICA,
            estado=datos_emergencia.get("estado", "programado"),
            usuario_id=reportado_por,
            especialidad=datos_emergencia.get("especialidad"),
            ubicacion=datos_emergencia.get("ubicacion"),
            notas=datos_emergencia.get("notas"),
            fecha_creacion=datetime.now(),
            codigo_emergencia=datos_emergencia["codigo_emergencia"],
            paciente_info=datos_emergencia.get("paciente_info"),
            equipo_medico=datos_emergencia.get("equipo_medico", []),
            recursos_necesarios=datos_emergencia.get("recursos_necesarios", [])
        )
        
        # Validar reglas de negocio
        errores = emergencia.validar_reglas_negocio()
        if errores:
            raise ValueError(f"Errores de validación: {', '.join(errores)}")
        
        return await self._evento_repository.crear(emergencia)
    
    async def obtener_calendario_medico(self, usuario_id: str, 
                                      fecha_inicio: date, 
                                      fecha_fin: date) -> List[EventoMedico]:
        """
        Obtiene el calendario médico de un usuario en un rango de fechas.
        """
        usuario = await self._usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        eventos = await self._evento_repository.listar_por_rango_fechas(fecha_inicio, fecha_fin)
        eventos_usuario = [e for e in eventos if e.usuario_id == usuario_id]
        
        # Ordenar por fecha y hora
        eventos_usuario.sort(key=lambda x: (x.fecha, x.hora_inicio))
        
        return eventos_usuario
    
    async def verificar_disponibilidad_medico(self, usuario_id: str, 
                                            fecha: date, 
                                            hora_inicio: time, 
                                            hora_fin: time) -> bool:
        """
        Verifica si un médico está disponible en un horario específico.
        """
        fecha_inicio_dt = datetime.combine(fecha, hora_inicio)
        fecha_fin_dt = datetime.combine(fecha, hora_fin)
        
        return not await self._evento_repository.verificar_conflicto_horario(
            usuario_id, fecha, fecha_inicio_dt, fecha_fin_dt
        )
    
    async def obtener_guardias_del_dia(self, fecha: date) -> dict:
        """
        Obtiene todas las guardias organizadas por turno para una fecha específica.
        """
        guardias = await self._evento_repository.listar_por_fecha(fecha)
        guardias_del_dia = [g for g in guardias if g.tipo == TipoEvento.GUARDIA]
        
        resultado = {
            "mañana": [],
            "tarde": [],
            "noche": []
        }
        
        for guardia in guardias_del_dia:
            if hasattr(guardia, 'turno'):
                usuario = await self._usuario_repository.buscar_por_id(guardia.usuario_id)
                info_guardia = {
                    "evento": guardia,
                    "medico": usuario.nombre_completo() if usuario else "Desconocido",
                    "especialidad": guardia.especialidad or "General"
                }
                resultado[guardia.turno].append(info_guardia)
        
        return resultado
    
    async def obtener_emergencias_activas(self) -> List[dict]:
        """
        Obtiene todas las emergencias activas con información del médico responsable.
        """
        emergencias = await self._evento_repository.listar_emergencias_activas()
        
        resultado = []
        for emergencia in emergencias:
            usuario = await self._usuario_repository.buscar_por_id(emergencia.usuario_id)
            info_emergencia = {
                "evento": emergencia,
                "medico_responsable": usuario.nombre_completo() if usuario else "Sin asignar",
                "tiempo_transcurrido": self._calcular_tiempo_transcurrido(emergencia)
            }
            resultado.append(info_emergencia)
        
        # Ordenar por prioridad y tiempo
        resultado.sort(key=lambda x: (
            x["evento"].prioridad.value,
            x["evento"].fecha_creacion
        ))
        
        return resultado
    
    async def _validar_limite_guardias_semanales(self, usuario_id: str, fecha: date):
        """
        Valida que un médico no exceda el límite de guardias por semana.
        """
        # Calcular inicio y fin de semana
        inicio_semana = fecha - timedelta(days=fecha.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        
        eventos_semana = await self._evento_repository.listar_por_rango_fechas(
            inicio_semana, fin_semana
        )
        
        guardias_usuario = [
            e for e in eventos_semana 
            if e.usuario_id == usuario_id and e.tipo == TipoEvento.GUARDIA
        ]
        
        # Límite de 3 guardias por semana
        if len(guardias_usuario) >= 3:
            raise ValueError("Límite de guardias semanales excedido (máximo 3)")
    
    def _calcular_tiempo_transcurrido(self, evento: EventoMedico) -> str:
        """
        Calcula el tiempo transcurrido desde la creación del evento.
        """
        delta = datetime.now() - evento.fecha_creacion
        
        if delta.days > 0:
            return f"{delta.days} días"
        elif delta.seconds > 3600:
            horas = delta.seconds // 3600
            return f"{horas} horas"
        else:
            minutos = delta.seconds // 60
            return f"{minutos} minutos"