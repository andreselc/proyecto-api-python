# Proyecto Final con DDD: Cadena de equipos electrónicos

Este proyecto utiliza el enfoque de Desarrollo Orientado al Dominio (DDD) para estructurar y organizar el código que permite gestionar productos, usuarios, órdenes y generar reportes básicos. Primero vas a encontrar instrucciones para poner el proyecto en funcionamiento.

# Instrucciones para Arrancar y Ejecutar el Proyecto

Este documento proporciona una guía paso a paso para arrancar y ejecutar el proyecto.

## Requisitos Previos

Asegúrate de tener instalados los siguientes programas en tu sistema:

1. **Docker** - Puedes descargarlo e instalarlo desde [aquí](https://www.docker.com/get-started).
2. **Docker Compose** - Normalmente viene incluido con la instalación de Docker.

## Construir y Ejecutar el Proyecto con Docker Compose

### Paso 1: Construir las Imágenes de Docker

Construye las imágenes de Docker especificadas en el archivo docker-compose.yml:

```bash
docker compose build
```

### Paso 2: Iniciar los Servicios

Inicia los servicios definidos en el archivo `docker-compose.yml`:

```bash
docker compose up
```

### Paso 3: Reiniciar los contenedores (en caso de cambios)

Este paso tambien sirve para ejecutar el paso 1 y 2 al mismo tiempo al momento de querer iniciar el archivo `docker-compose.yml`, creará los

```bash
docker-compose up -d --build
```

Este comando levantará los contenedores de la aplicación web, el manejador pgadmin y Postgresql. Sin embargo, se recomienda realizar los comandos por separado por mayor control de las cosas.

- La aplicación web estará disponible en http://localhost:8000
- El manejador pgadmin estará disponible en http://localhost:5050

## Para Ingresar a PgAdmin

### Paso 1: Ingresar las credenciales para autenticarse

Ingresar a la siguiente direccion http://localhost:5050 para poder autenticarse y acceder a la bd creada

```bash
PGADMIN_DEFAULT_EMAIL: admin@admin.com
PGADMIN_DEFAULT_PASSWORD: root
```

![](/Imagenes_readme/Inicio.png)

### Paso 2: Crear el server

El nombre que coloque es a su criterio

![](/Imagenes_readme/Paso1.1.png)
![](/Imagenes_readme/Paso2.png)

### Paso 3: Resgistrar los datos de la bd para conectarse

Una vez se registre un servidor, se colocaran las credenciales, de preferencia dejar por defecto el nombre de la base de datos que ya aparece por defecto que es "postgres" o crear un conexion para cada bd.
(En caso de decidir una sola conexion) Una vez haya cargado dele click a todas las bd para activarla y evitar errores (proyecto_fastapi y proyecto_fastapi_test)

```bash
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: proyecto_fastapi
HOST: db
PORT: 5432
```

![](/Imagenes_readme/Paso3.png)

## Para correr las pruebas

### Paso 1: Construir y Ejecutar el Proyecto con Docker Compose

### Paso 2: Ejecutar desde el contenedor las pruebas

Una vez este el docker levantado, desde el contenedor web se ejecutará el siguiente comando para ver el funcionamiento de la pruebas.

```bash
    docker-compose exec web pytest -v
```

## Para correr las migraciones

### Paso 1: Construir y Ejecutar el Proyecto con Docker Compose

### Paso 2: Ejecutar desde el contenedor las migraciones

En caso de que quiera crear alguna migracion por una modificacion, use el siguiente comando

```bash
docker-compose exec web alembic revision --autogenerate -m "Example model"
```

Para aplicar las migraciones use alguno de los siguientes comandos
Para correr todas las migraciones

```bash
docker-compose exec web alembic upgrade heads

```

Para correr la ultima migración o de un id en especifico

```bash
docker-compose exec web alembic upgrade head
docker-compose exec web alembic upgrade id_migracion
```

## Probar la Aplicación

Una vez que los contenedores estén en funcionamiento, puedes probar la aplicación utilizando un navegador web o herramientas como `curl` o `Postman`, o directamente con `Swagger`, que viene integrado en la aplicación, este último lo revisas en la dirección:

```bash
http://localhost:8000/docs
```

Tendrán disponible apenas corra la aplicacion un usuario (superadmin) default que permitira crear usuario de todo tipo y con ello pobrar la funcionalidad de cada endpoint

```bash
Username: superadmin
Password: ContraSupAdmin123
```
