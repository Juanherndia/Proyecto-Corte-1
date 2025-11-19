# Guía de Inicio Rápido - Planificador Médico v3.0

## 🚀 Instalación y Configuración

### Opción 1: Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd PlanificadorU

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 3. Iniciar servicios
docker-compose up -d

# 4. Verificar que todo funciona
curl http://localhost:5000/health
```

### Opción 2: Desarrollo Local

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar base de datos PostgreSQL
createdb planificador_medico

# 4. Ejecutar aplicación
cd backend
python app.py
```

## 🔧 Configuración Inicial

### Variables de Entorno Importantes

```bash
# Seguridad (CAMBIAR EN PRODUCCIÓN)
JWT_SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-32-chars-min
PASSWORD_HASH_ROUNDS=12

# Base de datos
DB_HOST=localhost
DB_NAME=planificador_medico
DB_USERNAME=postgres
DB_PASSWORD=tu-password-seguro

# CORS (ajustar según tu frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 📊 Primeros Pasos con la API

### 1. Verificar Estado del Sistema

```bash
curl http://localhost:5000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "service": "Planificador Médico API",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Registrar un Usuario Médico

```bash
curl -X POST http://localhost:5000/api/usuarios/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dr.garcia@hospital.com",
    "nombre": "Carlos",
    "apellido": "García",
    "especialidad": "Cardiología",
    "numero_licencia": "MED001",
    "telefono": "1234567891",
    "rol": "medico",
    "password": "MiPassword123!"
  }'
```

### 3. Autenticarse

```bash
curl -X POST http://localhost:5000/api/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dr.garcia@hospital.com",
    "password": "MiPassword123!"
  }'
```

Guarda el token JWT de la respuesta.

### 4. Acceder a Rutas Protegidas

```bash
# Usar el token obtenido en el paso anterior
curl -X GET http://localhost:5000/api/usuarios/me \
  -H "Authorization: Bearer TU-JWT-TOKEN-AQUI"
```

## 🏥 Usuarios de Prueba (Desarrollo)

El sistema incluye usuarios de prueba:

```
Admin:
- Email: admin@hospital.com
- Password: Admin123!
- Rol: administrador

Dr. García:
- Email: dr.garcia@hospital.com  
- Password: MedicoPass123!
- Rol: medico

Dra. Martínez:
- Email: dra.martinez@hospital.com
- Password: MedicoPass123!
- Rol: medico

Enfermera López:
- Email: enf.lopez@hospital.com
- Password: EnfermeraPass123!
- Rol: enfermero
```

## 🐳 Comandos Docker Útiles

```bash
# Ver logs de la aplicación
docker-compose logs -f planificador-api

# Reiniciar solo la API
docker-compose restart planificador-api

# Acceder al contenedor de la API
docker-compose exec planificador-api bash

# Ver estado de todos los servicios
docker-compose ps

# Limpiar volúmenes (CUIDADO: elimina datos)
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache
```

## 🔍 Troubleshooting

### Problema: Error de conexión a base de datos
```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps postgres

# Ver logs de PostgreSQL
docker-compose logs postgres

# Verificar variables de entorno
docker-compose exec planificador-api printenv | grep DB_
```

### Problema: Token JWT inválido
- Verificar que JWT_SECRET_KEY es consistente
- Verificar formato del header: `Authorization: Bearer <token>`
- El token expira en 24h por defecto

### Problema: CORS en el frontend
- Verificar CORS_ALLOWED_ORIGINS en .env
- Incluir el origen del frontend (ej: http://localhost:3000)

## 📱 Frontend (Próximos Pasos)

El frontend actual es básico HTML/CSS/JS. Para desarrollo moderno:

```bash
# Crear aplicación React
npx create-react-app planificador-frontend
cd planificador-frontend

# Instalar dependencias adicionales
npm install axios @mui/material @emotion/react @emotion/styled

# Configurar proxy para desarrollo (package.json)
"proxy": "http://localhost:5000"
```

## 🧪 Ejecutar Tests

```bash
# Tests unitarios
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Con cobertura
pytest --cov=src --cov-report=html
```

## 📈 Monitoreo

Con la configuración completa de Docker:

- **API**: http://localhost:5000
- **PgAdmin**: http://localhost:8080 (admin@planificador.com / admin123)
- **Grafana**: http://localhost:3000 (admin / admin)
- **Prometheus**: http://localhost:9090

## 🆘 Soporte

Si encuentras problemas:

1. Verificar logs: `docker-compose logs`
2. Revisar configuración de variables de entorno
3. Asegurarse de que todos los puertos están disponibles
4. Consultar la documentación en `docs/`

---

¡Listo para empezar a desarrollar! 🚀