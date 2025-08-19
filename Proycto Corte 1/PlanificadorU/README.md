# 1. Inicio / Presentación del proyecto

En el ámbito médico y de emergencias, la gestión eficiente de turnos, guardias, reuniones clínicas y alertas es fundamental para salvar vidas y optimizar recursos. Los profesionales enfrentan estrés y riesgos por mala organización, falta de comunicación y sobrecarga de tareas. Este sistema centraliza la gestión de horarios, tareas críticas y notificaciones en una herramienta web automatizada, confiable y rápida.

- [Presentación creativa](docs/Presentacion_Creativa.md)

# 2. Fundamentos de Ingeniería de Software

El sistema prioriza los siguientes atributos de calidad:

- **Confiabilidad**
- **Disponibilidad**
- **Usabilidad**
- **Mantenibilidad**
- **Reusabilidad**
- **Escalabilidad**

# 3. Diseño de software

## Principios SOLID aplicados y justificados

- **SRP:** La clase `Horario` gestiona únicamente los turnos y guardias médicas.
- **OCP:** Añadir nuevos tipos de alertas no requiere modificar el código base gracias a la interfaz `INotificador`.
- **DIP:** Las clases de alto nivel dependen de la abstracción `INotificador`.

## Patrones de diseño utilizados y justificación

- **Factory Method:** Para crear eventos médicos.
- **Observer:** Para notificaciones automáticas.

## UML

- [Diagrama de clases UML (PlantUML)](PlanificadorU\docs\UML.png)


# 4. Implementación

## Estructura del código y enlaces explicativos

- `/src/modelo`: Clases principales
- `/src/notificaciones`: Interfaces y clases de notificación
- `/src/factoria`: Factory Method
- `/web`: Interfaz visual
- `/backend`: Lógica y API Flask

## Ejemplo de uso (backend)

```python
from src.factoria.EventoFactory import EventoFactory
guardia = EventoFactory.crear_evento("guardia", nombre="Guardia Nocturna", fecha="2025-08-20", hora="22:00", especialidad="Urgencias")
print(guardia.mostrar_info())
emergencia = EventoFactory.crear_evento("emergencia", nombre="Emergencia Cardiaca", fecha="2025-08-20", hora="03:00", descripcion="Paciente con paro cardíaco")
print(emergencia.mostrar_info())
```

## Ejemplo de uso (frontend)

```js
fetch("http://localhost:5000/api/evento", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    tipo: "guardia",
    nombre: "Guardia Nocturna",
    fecha: "2025-08-20",
    hora: "22:00",
    especialidad: "Urgencias",
  }),
});
```

# 5. Análisis técnico

- [Análisis técnico detallado](docs/Analisis_Tecnico.md)

# 6. Créditos y roles del equipo

- Jacobo Andrés Pacheco Martínez (ID 0000260017): Arquitecto de Software y Líder Técnico
- Juan Camilo Hernández Díaz (ID 0000308561): Desarrollador Backend y Especialista en Integración
- Juan Felipe Jaime (ID 0000243671): Desarrollador Frontend y Experiencia de Usuario
