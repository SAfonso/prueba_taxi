# Proyecto de Análisis de Viajes con Pandas

Este proyecto procesa datos de viajes para generar informes semanales y mensuales utilizando Python y Pandas. Los resultados se almacenan en un archivo CSV y un archivo Excel.

## Estructura del Proyecto

yellow_taxi/
├── data/                        # Carpeta de datos de entrada
│   ├── yellow_tripdata_2022-01.parquet
│   ├── yellow_tripdata_2022-02.parquet
│   └── yellow_tripdata_2022-03.parquet
├── output/                      # Carpeta para guardar los informes generados
│   ├── bad_data                  # Carpeta para guardar los informes generados con datos erroneos
├── src/
│   ├── main.py                  # Archivo principal del proyecto
│   ├── data_process.py          # Funciones de procesamiento de datos
│   └── utils.py                 # Funciones auxiliares (ej. lectura de archivos)
└── requirements.txt             # Lista de dependencias

## Configuración del Entorno

### Prerrequisitos

- **Python 3.12**
- **pip**: Administrador de paquetes para instalar dependencias
- **Entorno virtual**: Recomendado para instalar las dependencias sin afectar otros proyectos

### Instalación y Configuración

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/usuario/prueba_taxi.git
   cd proyecto_viajes

2. **Crear entorno virtual:**
    python -m venv venv
    venv\Scripts\activate
   
3. **Instalar dependencias:**
   pip install -r requirements.txt

4. **Ejecutar:**
   python src/main.py

**Archivos de Salida**
*agregadoSemanal.csv:* Informe con agregados semanales.
*agregadoMensual.xlsx:* Informe con agregados mensuales y tres pestañas (JFK, Regular, Others).

