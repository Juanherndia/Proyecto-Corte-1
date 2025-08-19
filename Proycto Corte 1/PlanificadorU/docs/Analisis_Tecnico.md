# Análisis Técnico

## Cohesión

Cada clase tiene una responsabilidad clara: `Horario` gestiona turnos y guardias médicas, `Evento` representa actividades críticas (guardias, emergencias, reuniones), y los notificadores se encargan de enviar avisos por distintos canales.

## Bajo Acoplamiento

Las clases dependen de interfaces y abstracciones (`INotificador`), permitiendo cambiar la forma de notificación (app, email, SMS) sin modificar el resto del sistema. El backend y frontend están desacoplados mediante API REST.

## Atributos de Calidad

- **Confiabilidad:** El sistema debe funcionar correctamente en situaciones críticas y emergencias.
- **Disponibilidad:** Acceso rápido y seguro desde cualquier dispositivo, incluso en guardias nocturnas.
- **Usabilidad:** Interfaz intuitiva para médicos y personal de emergencias, con notificaciones automáticas.
- **Mantenibilidad:** Arquitectura modular y código comentado.
- **Reusabilidad:** Componentes reutilizables en otros contextos médicos.
- **Escalabilidad:** Fácil de agregar nuevos tipos de eventos y notificadores.

## Cumplimiento de la Rúbrica

- Principios SOLID aplicados y justificados en el diseño y código.
- Patrones de diseño implementados y documentados.
- Diagrama UML consistente con el código y el contexto médico/emergencias.
