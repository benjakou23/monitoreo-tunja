# Proyecto de Monitoreo - Tunja

Este repositorio contiene el código fuente para el sistema de monitoreo basado en microservicios.

## Integrantes
* Sara Sofía Lizarazo Barrera
* Laura Daniela Vargas Acero
* Anderson Benjamín Girón Villegas
* Mendoza Vega Carlos Yair


## Arquitectura de Microservicios
El sistema está compuesto por los siguientes servicios:
* **Auth Service:** Gestión de autenticación.
* **Users Service:** Administración de usuarios y roles.
* **Devices Service:** Monitoreo de dispositivos.
* **Alerts Service:** Sistema de notificaciones y alertas.
* **Locations Service:** Gestión geográfica de puntos de monitoreo.
* **Metrics Service:** Procesamiento de datos y métricas.

## Vista Previa del Uso
### Backend y Microservicios
Aquí se observa la ejecución del servicio de usuarios y la creación de tablas en la base de datos:
1.
![alt text]({DD77F915-7E8D-4CDC-BC31-1737716C3A42}.png)
2.
![alt text]({D1BDCA37-8C79-4839-A81B-22E22EA5D266}.png)
3.
![alt text]({9893A5AA-8A3B-4204-90AD-27877FD2CF30}.png)
4.
![alt text]({A3120BE2-DC0C-4E9C-9A2E-56DCEC9E91B7}.png)
5.
![alt text]({BBE827E6-705D-4D89-990F-54C57ECA05B8}.png)
6.
![alt text]({FEE3DE94-8CEB-414E-BFF7-620B72D9707B}.png)



### Frontend
El frontend se sirve de forma independiente para interactuar con los microservicios:
![alt text]({0AF92EC1-BF1C-4BFB-B0CB-71371499B193}.png)

## Cómo ejecutar el proyecto
1. Clonar el repositorio.
2. Configurar los entornos virtuales para cada microservicio.
3. Ejecutar `python run.py` dentro de cada carpeta de servicio.
4. Para el frontend, usar un servidor local (ej. `python -m http.server 3000`).