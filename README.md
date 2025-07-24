# Restaurant API - Proyecto Fullstack

Este proyecto incluye un backend con Flask y un frontend con React para la gestión de reservas en restaurantes.

Repositorio:
[https://github.com/Nicolasmateoprietojimenez/restaurantapi](https://github.com/Nicolasmateoprietojimenez/restaurantapi)

---

## Requisitos previos

* Python
* Node.js + npm
* Git

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/Nicolasmateoprietojimenez/restaurantapi.git
cd restaurantapi
```

---

## 2. Crear y activar un entorno virtual

### En Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### En Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Ejecutar el backend

En la primera terminal, con el entorno virtual activado:

```bash
python run.py
```

Esto levanta el servidor Flask en:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 5. Ejecutar el frontend

En una segunda terminal:

```bash
cd client-api
npm install
npm start
```

Esto levanta la aplicación React en:
[http://localhost:3000/](http://localhost:3000/)

---

## Accesos y pruebas

### CRUD de administración:

[http://127.0.0.1:5000/admin/](http://127.0.0.1:5000/admin/)

### Endpoints de la API REST:

Todos siguen la estructura:

```
http://127.0.0.1:5000/<modelo_en_plural>
```

Modelos disponibles:

* /restaurantes
* /mesas
* /clientes
* /reservas
* /fotos
* /comentarios

Ejemplos:

* GET [http://127.0.0.1:5000/restaurantes](http://127.0.0.1:5000/restaurantes)
* POST para crear
* PUT para actualizar
* DELETE para eliminar

---

## Interfaz del cliente (React)

[http://localhost:3000/](http://localhost:3000/)

### Usuarios de prueba:

```json
{
  "nombre": "Carlos Rodríguez",
  "email": "carlos.rodriguez@example.com",
  "telefono": "3101112233",
  "contrasena": "carlos789"
},
{
  "nombre": "Laura Martínez",
  "email": "laura.martinez@example.com",
  "telefono": "3209998877",
  "contrasena": "laura321"
},
{
  "nombre": "Andrés López",
  "email": "andres.lopez@example.com",
  "telefono": "3011122233",
  "contrasena": "andres456"
}
```

Una vez logeado, el cliente puede hacer reservas.

---

## Script de prueba de reservas simultáneas

Con el entorno virtual activado y estando en la raíz del proyecto:

```bash
python script.py
```

Esto ejecuta un script que simula varias reservas simultáneas para un restaurante y prueba el funcionamiento del API.

---

## Listo para probar

Una vez ambos servidores estén activos ([http://127.0.0.1:5000/](http://127.0.0.1:5000/) y [http://localhost:3000/](http://localhost:3000/)), ya se puede probar toda la funcionalidad del sistema.
