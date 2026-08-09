# Proyecto_MeteoCaracas_2627-I - Sistema de Análisis Meteorológico
Se ha solicitado el desarrollo de un proyecto, ejecutado estrictamente bajo el enfoque de la Programación Orientada a Objetos (POO), usando el lenguaje de programación Python. Con el fin de desarrollar un sistema de monitoreo y consulta del clima en el área Metropolitana de Caracas, en tiempo real.

MeteoCaracas es una aplicación de consola desarrollada en Python que permite consultar, analizar y graficar datos meteorológicos de diversas localidades del área metropolitana de Caracas. El sistema consume datos en tiempo real e históricos a través de la API de **Open-Meteo**.

# Características Principales

* Carga Dinámica de Datos: Parseo de zonas y localidades mediante archivos JSON implementando un modelo estricto de Programación Orientada a Objetos (POO).
* Consultas en Tiempo Real: Búsqueda del clima actual (temperatura, humedad, viento, precipitación) por búsqueda directa o selección guiada.
* Estadísticas de Sesión: Cálculo de la localidad más cálida, más fría y el promedio de temperatura global de las consultas activas.
* Análisis Histórico y Visualización: Integración con la API de Open-Meteo para generar reportes históricos y gráficos de evolución climática utilizando `matplotlib`.
* Reporte de Cobertura: Identificación de localidades sin coordenadas geográficas válidas (`null`).

# Tecnologías y Librerías Utilizadas

El proyecto fue construido utilizando únicamente las librerías permitidas por los lineamientos de la evaluación:
* **Python 3.x**
* `requests`: Para el consumo de la API REST de Open-Meteo.
* `matplotlib`: Para la renderización de gráficos históricos.
* `json`: Para la lectura y estructuración de la base de datos local.

# Arquitectura del Proyecto

PROYECTO_METEOCARACAS_2627-I/
│
├── core/
│   ├── __init__.py
│   ├── analizador.py
│   ├── api_client.py
│   ├── cargador.py
│   ├── gestor_consultas.py
│   ├── modelos.py
│   ├── registro.py
│   └── reportes.py
│
├── models/
│   ├── ClimaActual.py
│   ├── Estadisticas.py
│   ├── Localidad.py
│   ├── Municipio.py
│   └── RegistroHistorico.py
│
├── main.py
├── proyecto 2526-int.docx.pdf
├── README.md
└── zonas_caracas.json

*Datos de los Integrantes:*
   * Ana Mercedes Cabrera /C.I. 32.122.147 / Carnet: 20251110058
   * Elena Sanchez /C.I. 31.874.786 /20241110245 
   * Cristian Pisano /C.I. 34.559.130 / 20261110583
   
 *Datos de la Asignatura y Sección:*
   * Nombre de la materia: Algoritmos y Programacion
   * Período o Trimestre: 2526-INT
   * Sección: 2
   * Prof. Christian Guillen
   * Preparadores: Christian Sanchez y Diego Arreaza
  