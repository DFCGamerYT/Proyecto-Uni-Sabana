# Proyecto Uni Sabana -- Implementación DevOps

## 📌 Descripción General

Este proyecto corresponde a una implementación académica orientada a
prácticas modernas de **DevOps**, integrando desarrollo de software,
contenerización, automatización de pruebas e integración continua.

El objetivo principal es demostrar la aplicación de herramientas como:

-   Python
-   Docker
-   Docker Compose
-   Jenkins
-   GitHub Actions
-   Pytest

El proyecto está diseñado bajo principios de:

-   Integración Continua (CI)
-   Automatización
-   Reproducibilidad
-   Contenerización
-   Buenas prácticas de versionamiento

------------------------------------------------------------------------

# 🏗 Arquitectura del Proyecto

## 🔷 Arquitectura General


            ┌──────────────────────┐
            │      Desarrollador   │
            └─────────────┬────────┘
                          │ git push
                          ▼
            ┌────────────────────────────┐
            │        GitHub Repo         │
            └─────────────┬──────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
     ┌─────────────────┐     ┌─────────────────┐
     │ GitHub Actions  │     │     Jenkins     │
     │ (CI automática) │     │  Pipeline CI/CD │
     └────────┬────────┘     └────────┬────────┘
              │                       │
              ▼                       ▼
         Ejecuta Tests           Build Docker Image
              │                       │
              └──────────────┬────────┘
                             ▼
                     ┌────────────────┐
                     │  Docker Image  │
                     └────────┬───────┘
                              ▼
                     ┌────────────────┐
                     │   Contenedor   │
                     └────────────────┘

------------------------------------------------------------------------

# 📂 Estructura del Proyecto

    Proyecto-Uni-Sabana/
    │
    ├── .github/               # Workflows de GitHub Actions (CI)
    ├── Dockerfile             # Definición de la imagen Docker
    ├── docker-compose.yml     # Orquestación de contenedores
    ├── Jenkinsfile            # Pipeline CI/CD en Jenkins
    ├── main.py                # Aplicación principal
    ├── requirements.txt       # Dependencias Python
    ├── test_main.py           # Pruebas automatizadas
    └── .gitignore             # Archivos ignorados por Git

------------------------------------------------------------------------

# 🧩 Componentes DevOps Explicados

## 1️⃣ Aplicación -- `main.py`

Contiene la lógica principal del sistema desarrollada en Python. Es el
punto de entrada de ejecución del contenedor.

------------------------------------------------------------------------

## 2️⃣ Dependencias -- `requirements.txt`

Define las librerías necesarias para ejecutar la aplicación. Permite
reproducibilidad del entorno.

------------------------------------------------------------------------

## 3️⃣ Pruebas Automatizadas -- `test_main.py`

Implementadas con **Pytest**, validan el comportamiento de la
aplicación. Se ejecutan automáticamente en los pipelines CI.

------------------------------------------------------------------------

## 4️⃣ Contenerización -- `Dockerfile`

Define el proceso para construir una imagen Docker:

1.  Selección de imagen base Python
2.  Copia del código fuente
3.  Instalación de dependencias
4.  Definición del comando de ejecución

Beneficios: - Portabilidad - Aislamiento - Consistencia entre entornos

------------------------------------------------------------------------

## 5️⃣ Orquestación -- `docker-compose.yml`

Permite ejecutar el proyecto con un solo comando. Facilita:

-   Configuración de puertos
-   Variables de entorno
-   Escalabilidad futura

------------------------------------------------------------------------

## 6️⃣ Integración Continua -- GitHub Actions

Ubicados en `.github/workflows`.

Automatiza: - Ejecución de pruebas en cada push - Validación de Pull
Requests - Control de calidad del código

------------------------------------------------------------------------

## 7️⃣ Pipeline CI/CD -- Jenkinsfile

Define las etapas del pipeline:

-   Checkout del código
-   Instalación de dependencias
-   Ejecución de pruebas
-   Construcción de imagen Docker
-   Despliegue (si aplica)

Permite automatizar completamente el ciclo de vida del software.

------------------------------------------------------------------------

# 🚀 Guía Paso a Paso para Montar el Proyecto

------------------------------------------------------------------------

## 🔹 Opción 1: Ejecución Local (Sin Docker)

### 1. Clonar el repositorio

    git clone https://github.com/DFCGamerYT/Proyecto-Uni-Sabana.git
    cd Proyecto-Uni-Sabana

### 2. Crear entorno virtual

    python -m venv venv
    source venv/bin/activate      (Linux/Mac)
    venv\Scripts\activate       (Windows)

### 3. Instalar dependencias

    pip install -r requirements.txt

### 4. Ejecutar aplicación

    python main.py

------------------------------------------------------------------------

## 🔹 Opción 2: Ejecución con Docker

### 1. Construir imagen

    docker build -t proyecto-uni-sabana .

### 2. Ejecutar contenedor

    docker run -p 5000:5000 proyecto-uni-sabana

------------------------------------------------------------------------

## 🔹 Opción 3: Ejecución con Docker Compose (Recomendado)

### 1. Levantar servicios

    docker compose up --build

### 2. Acceder a la aplicación

    http://localhost:5000

------------------------------------------------------------------------

# 🧪 Ejecución de Pruebas

    pytest

O dentro del contenedor:

    docker run proyecto-uni-sabana pytest

------------------------------------------------------------------------

# 📊 Buenas Prácticas DevOps Aplicadas

✔ Control de versiones con Git\
✔ Automatización de pruebas\
✔ Integración Continua\
✔ Contenerización\
✔ Infraestructura reproducible\
✔ Separación de responsabilidades

------------------------------------------------------------------------

# 📚 Conclusión

Este proyecto demuestra la implementación práctica de principios DevOps
en un entorno académico, integrando desarrollo, automatización y
despliegue continuo.

Permite comprender el flujo completo:

Desarrollo → Versionamiento → Pruebas → Build → Contenerización →
Ejecución

------------------------------------------------------------------------

## 👨‍💻 Proyecto Académico

Integrantes: Andres Meneses, David Cifuentes, David Monsalve
Universidad de La Sabana
Maestría en Arquitectura de Software
Materia: Fundamentos DevOps MAS-MIS 2026-1
Actividad 3. Laboratorio técnico U2
