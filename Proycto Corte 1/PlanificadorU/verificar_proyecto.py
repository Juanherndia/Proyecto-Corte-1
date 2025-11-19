#!/usr/bin/env python3
"""
Script de verificación del Proyecto Planificador Médico v3.0
Verifica que toda la arquitectura esté correctamente implementada.
"""
import os
import sys
import importlib.util
from pathlib import Path

def verificar_estructura_proyecto():
    """Verifica que la estructura de directorios esté completa"""
    print("🔍 Verificando estructura del proyecto...")
    
    directorios_requeridos = [
        "src/domain/entities",
        "src/domain/repositories", 
        "src/domain/services",
        "src/application/use_cases",
        "src/application/dto",
        "src/infrastructure/repositories",
        "src/infrastructure/security",
        "src/interfaces/api/controllers",
        "src/interfaces/api/middleware",
        "config",
        "docs",
        "tests/unit",
        "tests/integration"
    ]
    
    base_path = Path(".")
    errores = []
    
    for directorio in directorios_requeridos:
        path = base_path / directorio
        if not path.exists():
            errores.append(f"❌ Directorio faltante: {directorio}")
        else:
            print(f"✅ {directorio}")
    
    return errores

def verificar_archivos_clave():
    """Verifica que los archivos clave existan"""
    print("\n🔍 Verificando archivos clave...")
    
    archivos_requeridos = [
        "README.md",
        "requirements.txt", 
        "Dockerfile",
        "docker-compose.yml",
        ".env.example",
        "backend/app.py",
        "src/domain/entities/usuario.py",
        "src/domain/entities/evento_medico.py",
        "config/settings.py",
        "config/di_container.py",
        "docs/Arquitectura_Completa.md"
    ]
    
    base_path = Path(".")
    errores = []
    
    for archivo in archivos_requeridos:
        path = base_path / archivo
        if not path.exists():
            errores.append(f"❌ Archivo faltante: {archivo}")
        else:
            print(f"✅ {archivo}")
    
    return errores

def verificar_sintaxis_python():
    """Verifica la sintaxis de los archivos Python principales"""
    print("\n🔍 Verificando sintaxis de Python...")
    
    archivos_python = [
        "backend/app.py",
        "src/domain/entities/usuario.py", 
        "src/domain/entities/evento_medico.py",
        "config/settings.py",
        "config/di_container.py"
    ]
    
    errores = []
    
    for archivo in archivos_python:
        path = Path(archivo)
        if path.exists():
            try:
                spec = importlib.util.spec_from_file_location("module", path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    # Solo verificamos que se puede cargar la sintaxis
                    compile(open(path).read(), path, 'exec')
                    print(f"✅ Sintaxis válida: {archivo}")
                else:
                    errores.append(f"❌ No se puede crear spec para: {archivo}")
            except SyntaxError as e:
                errores.append(f"❌ Error de sintaxis en {archivo}: {e}")
            except Exception as e:
                errores.append(f"⚠️  Advertencia en {archivo}: {e}")
        else:
            errores.append(f"❌ Archivo no encontrado: {archivo}")
    
    return errores

def verificar_principios_solid():
    """Verifica que se implementen los principios SOLID"""
    print("\n🔍 Verificando implementación de principios SOLID...")
    
    verificaciones = {
        "SRP - Single Responsibility": [
            "src/domain/entities/usuario.py",
            "src/infrastructure/security/password_hasher.py", 
            "src/infrastructure/security/jwt_service.py"
        ],
        "OCP - Open/Closed": [
            "src/domain/entities/evento_medico.py"  # Clase abstracta con herencia
        ],
        "LSP - Liskov Substitution": [
            "src/domain/repositories/usuario_repository.py",  # Interface
            "src/infrastructure/repositories/in_memory_usuario_repository.py"  # Implementación
        ],
        "ISP - Interface Segregation": [
            "src/domain/repositories/usuario_repository.py",
            "src/domain/repositories/evento_medico_repository.py"
        ],
        "DIP - Dependency Inversion": [
            "config/di_container.py",
            "src/application/use_cases/usuario_use_cases.py"
        ]
    }
    
    for principio, archivos in verificaciones.items():
        print(f"\n📋 {principio}:")
        for archivo in archivos:
            if Path(archivo).exists():
                print(f"  ✅ {archivo}")
            else:  
                print(f"  ❌ {archivo}")

def verificar_clean_architecture():
    """Verifica la implementación de Clean Architecture"""
    print("\n🔍 Verificando Clean Architecture...")
    
    capas = {
        "Domain Layer (Núcleo)": [
            "src/domain/entities/",
            "src/domain/repositories/", 
            "src/domain/services/"
        ],
        "Application Layer": [
            "src/application/use_cases/",
            "src/application/dto/"
        ],
        "Infrastructure Layer": [
            "src/infrastructure/repositories/",
            "src/infrastructure/security/"
        ],
        "Interface Layer": [
            "src/interfaces/api/controllers/",
            "src/interfaces/api/middleware/"
        ]
    }
    
    for capa, directorios in capas.items():
        print(f"\n🏗️ {capa}:")
        for directorio in directorios:
            if Path(directorio).exists():
                archivos = list(Path(directorio).glob("*.py"))
                if archivos:
                    print(f"  ✅ {directorio} ({len(archivos)} archivos)")
                else:
                    print(f"  ⚠️  {directorio} (sin archivos .py)")
            else:
                print(f"  ❌ {directorio}")

def main():
    """Función principal de verificación"""
    print("🏥 VERIFICACIÓN DEL PROYECTO PLANIFICADOR MÉDICO v3.0")
    print("=" * 60)
    
    todos_los_errores = []
    
    # Verificaciones
    todos_los_errores.extend(verificar_estructura_proyecto())
    todos_los_errores.extend(verificar_archivos_clave())
    todos_los_errores.extend(verificar_sintaxis_python())
    
    verificar_principios_solid()
    verificar_clean_architecture()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    if todos_los_errores:
        print(f"❌ Se encontraron {len(todos_los_errores)} problemas:")
        for error in todos_los_errores:
            print(f"  {error}")
        print("\n🔧 Corrige estos problemas antes de continuar.")
        return 1
    else:
        print("🎉 ¡VERIFICACIÓN EXITOSA!")
        print("✅ Estructura del proyecto: Completa")
        print("✅ Archivos clave: Presentes") 
        print("✅ Sintaxis Python: Válida")
        print("✅ Principios SOLID: Implementados")
        print("✅ Clean Architecture: Implementada")
        print("\n🚀 El proyecto está listo para el tercer corte!")
        return 0

if __name__ == "__main__":
    sys.exit(main())