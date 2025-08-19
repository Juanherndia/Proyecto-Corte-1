# Proyecto de Diseño de Software – Corte Uno

## 🧠 Presentación del Problema
Muchos estudiantes universitarios tienen dificultades para organizar sus horarios de estudio, clases y proyectos. Esto genera estrés, incumplimiento de entregas y mala gestión del tiempo. Nuestro sistema, **Planificador U**, busca centralizar la gestión académica en una herramienta simple y automatizada.

## 🎨 Creatividad en la Presentación
Presentamos un video tipo “diario de estudiante” donde se muestran los retos diarios de gestión del tiempo y cómo Planificador U transforma la experiencia.
🎥 https://youtu.be/planificador-u-demo

## 🧱 Fundamentos de Ingeniería de Software
Nuestro sistema prioriza los siguientes atributos de calidad:
- **Usabilidad**: interfaz amigable y simple para estudiantes.
- **Mantenibilidad**: arquitectura modular con responsabilidades bien separadas.
- **Reusabilidad**: componentes de planificación y notificación reutilizables en otros contextos.

## 🧩 Diseño de Software

### Principios SOLID aplicados:
- **SRP**: La clase `Horario` se encarga únicamente de gestionar franjas de tiempo.
- **OCP**: Añadir nuevos tipos de recordatorios no requiere modificar el código base gracias a la interfaz `Notificador`.
- **DIP**: Las clases de alto nivel dependen de la abstracción `INotificador`, no de implementaciones concretas.

### Patrones de Diseño utilizados:
- **Factory Method**: para crear diferentes tipos de eventos (`Clase`, `Tarea`, `Examen`) desde una interfaz común.
- **Observer**: el usuario se suscribe a eventos de cambio en su calendario y recibe notificaciones automáticas.

### UML:
![Diagrama de clases UML](https://i.imgur.com/uml-ejemplo.png)

## 💻 Implementación
El código está estructurado en paquetes:
- `/modelo` contiene clases como `Evento`, `Horario`, `Tarea`, `Examen`.
- `/notificaciones` contiene `INotificador`, `EmailNotificador`, `AppNotificador`.
- `/factoria` contiene la implementación del Factory Method.

## 🔍 Análisis Técnico
El sistema presenta:
- **Alta cohesión**: cada clase tiene una responsabilidad clara.
- **Bajo acoplamiento**: gracias al uso de interfaces y la inversión de dependencias.
- Se consideran atributos como escalabilidad futura al permitir extensiones sin modificar las clases existentes.

## 👥 Créditos y Roles
- Carlos Pérez – Diseño UML y lógica de negocio
- Andrés López – Implementación de patrones y pruebas
- Sara Carolina – Creatividad y video de presentación