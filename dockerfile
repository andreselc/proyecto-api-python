# Partimos de una base oficial de python
FROM python:3.12-slim

# El directorio de trabajo es desde donde se ejecuta el contenedor al iniciarse
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat-openbsd gcc postgresql \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
  # Copiar todo desde el contexto de construcción al directorio de trabajo en la imagen
COPY requirements.txt requirements.txt
#corre e intalas todo lo que tenga en mi requeriments.txt
RUN pip install -r requirements.txt

# add app
COPY . .

