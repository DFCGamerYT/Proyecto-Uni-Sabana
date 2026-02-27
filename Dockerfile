# Etapa 1: Imagen base de Jenkins (LTS) — usada para ejecutar Jenkins
FROM jenkins/jenkins:lts

# Cambia a usuario root para instalar paquetes del sistema
USER root

# Actualiza índices de apt e instala 'lsb-release' (necesario para obtener el nombre de la distribución)
RUN apt-get update && apt-get install -y lsb-release

# Descarga la clave GPG oficial de Docker y la guarda en el keyring del sistema
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg

# Agrega el repositorio oficial de Docker para la arquitectura y codename de la distro
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

# Actualiza nuevamente e instala solo el cliente de Docker (docker-ce-cli)
RUN apt-get update && apt-get install -y docker-ce-cli

# Restablece el usuario no privilegiado 'jenkins' para ejecutar el servicio
USER jenkins

# ---------------------------------------------------------------
# Etapa 2: Imagen para la aplicación Python (multi-stage build separada)
# ---------------------------------------------------------------
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias (ruido mínimo entre etapas)
COPY requirements.txt .

# Instala las dependencias de Python sin cache para reducir tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Indica que la aplicación escuchará en el puerto 8000
EXPOSE 8000

# Comando por defecto: ejecutar la aplicación con Uvicorn en 0.0.0.0:8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]