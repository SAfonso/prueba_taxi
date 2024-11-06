import pandas as pd
from data_process import *
from utils import *

if __name__ == "__main__":

    print('Leyendo ficheros..')
    # Cargamos los datos desde los archivos Parquet proporcionados
    file_paths = [
        '../data/yellow_tripdata_2022-01.parquet',
        '../data/yellow_tripdata_2022-02.parquet',
        '../data/yellow_tripdata_2022-03.parquet'
    ]
    dataOriginal = readFilesFromList (file_paths)
    print('Lectura correcta')

    print('Cambiando formato de fechas...')
    # Cambiamos el formato de las fechas
    dataParsedDates = parseDates(dataOriginal)

    print('Generando campos temporales...')
    # Generamos el tiempo en segundos
    dataTimeSec = getDurationSec(dataParsedDates)

    # Generamos los campos yyyy-mm y yyyy-www
    dataMW = getYearsMonth(dataTimeSec)
    print('Campos creados correctamente.')

    print('Generando ficheros erroneos...')
    # Generamos los ficheros con los registros erroneos
    badFiles(dataMW)
    print('Check!')

    print('Rellenando valores nulos...')
    # Seteamos con valores por defecto los campos vacios
    dataFilled = setDefaultValues(dataMW)

    print('Obteniendo datos limpios...')
    # Obtenemos el conjunto de datos final
    dataCleaned = getDatCleaned(dataFilled)

    print('Empezamos!')
    print('Generando informe semanal...')
    # Generamos el informe semanal
    generar_informe_semanal(dataCleaned)
    print('Informe semanal generado.')

    # Obtenemos el campo day_type
    dataDType = getDayType(dataCleaned)

    print('Generando informe mensual...')
    # Generamos el informe mensual
    generar_informe_mensual(dataDType)
    print('Informe mensual generado.')
    print('Fin!')


