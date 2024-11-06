import pandas as pd
from utils import writeFilterCSV

def parseDates (data):
#  Pasamos los campos de fecha a dateTime

    data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
    data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])

    return data

def getDurationSec (data):
# Definir el  tiempo en segundos

    data['trip_duration_sec'] = (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds()

    return data

def getDayType (data):
# Definir tipo de día (1 para lunes a viernes, 2 para fin de semana)

    data['day_type'] = data['tpep_pickup_datetime'].dt.weekday.apply(lambda x: 1 if x < 5 else 2)

    return data


def getYearsMonth (data):

    data['year_week'] = data['tpep_pickup_datetime'].dt.strftime('%Y-0%U')
    data['year_month'] = data['tpep_pickup_datetime'].dt.strftime('%Y-%m')

    return data


def badFiles (data):
#  Creamos ficheros con los registros erroneos
# un fichero por cada caso que se ha detectado

    # Registros con campos negativos en el precio del trayecto, posible fraude
    precio_negativo = data[data['fare_amount'] < 0]
    writeFilterCSV(precio_negativo, 'precio_negativo.csv', '../output/bad_data')

    # Registros con campos negativos en el tiempo,
    # la activacion/desactivacion del taximetro no tiene sentido
    tiempo_negativo = data[data['trip_duration_sec'] < 0.1]
    writeFilterCSV(tiempo_negativo, 'tiempo_negativo.csv', '../output/bad_data')

    # Registros de otros años
    fecha_fuera_2022 = data[data['tpep_pickup_datetime'].dt.year != 2022]
    writeFilterCSV(fecha_fuera_2022, 'fecha_fuera_2022.csv', '../output/bad_data')

    # Registros con campos nulos o erroneos en RatecodeID
    ratecode_nulo = data[data['RatecodeID'].isnull()]
    writeFilterCSV(ratecode_nulo, 'ratecode_Nulo.csv', '../output/bad_data')

    # Registros con campos nulos o erroneos en RatecodeID
    ratecode_99 = data[data['RatecodeID'] == 99.0]
    writeFilterCSV(ratecode_99, 'ratecode_99.csv', '../output/bad_data')


def setDefaultValues (data):
#  Rellenamos los valores nulos que puedan existir
# en los campos en los que se han detectado nulos

    data['airport_fee'] = data['airport_fee'].fillna(0.0)
    data['congestion_surcharge'] = data['congestion_surcharge'].fillna(0.0)

    # Pondremos por defecto que hay conección
    data['store_and_fwd_flag'] = data['store_and_fwd_flag'].fillna('N')

    # Por defecto que lleva a un pasajero ya que es el mínimo indispensable
    data['passenger_count'] = data['passenger_count'].fillna(1)

    return data

def getDatCleaned (data):
#  Limpiamos los datos de los registros con posibles fallos

    dataCleanedAmount = data[
        (data['trip_duration_sec'] >= 0.1) &
        (data['trip_distance'] >= 0) &
        (data['fare_amount'] >= 0)
        ]

    dataCleaned = dataCleanedAmount[
        (dataCleanedAmount['tpep_pickup_datetime'].dt.year == 2022) &
        (dataCleanedAmount['year_month'] <= '2022-03') &
        (dataCleanedAmount['RatecodeID'].notnull()) &
        (dataCleanedAmount['RatecodeID'] != 99.0)
        ]

    return dataCleaned


def getJFKData(data):
    # Obtener los datos mensuales correspondientes al RatecodeID JFK

    jfk_data = data[data['RatecodeID'] == 2].groupby(['year_month', 'day_type']).agg(
        services=('tpep_pickup_datetime', 'count'),
        total_distance=('trip_distance', 'sum'),
        total_passengers=('passenger_count', 'sum')
    ).reset_index()

    return jfk_data


def getRegularData(data):
    # Obtener los datos mensuales correspondientes al RatecodeID Regular

    regular_data = data[data['RatecodeID'] == 1].groupby(['year_month', 'day_type']).agg(
        services=('tpep_pickup_datetime', 'count'),
        total_distance=('trip_distance', 'sum'),
        total_passengers=('passenger_count', 'sum')
    ).reset_index()

    return regular_data

def getOtherData(data):
    # Obtener los datos mensuales correspondientes al resto de RatecodeID

    other_data = data[~data['RatecodeID'].isin([1, 2])].groupby(['year_month', 'day_type']).agg(
        services=('tpep_pickup_datetime', 'count'),
        total_distance=('trip_distance', 'sum'),
        total_passengers=('passenger_count', 'sum')
    ).reset_index()

    return other_data


##########################################################################################
##########################################################################################


def generar_informe_semanal(data):
# Realizar agregaciones semanales y cálculos para el CSV
# y escribe el CSV correspondiente

    agregado_semanal_df = data.groupby('year_week').agg(
        min_trip_time=('trip_duration_sec', 'min'),
        max_trip_time=('trip_duration_sec', 'max'),
        avg_trip_time=('trip_duration_sec', 'mean'),
        min_distance=('trip_distance', 'min'),
        max_distance=('trip_distance', 'max'),
        avg_distance=('trip_distance', 'mean'),
        min_fare=('fare_amount', 'min'),
        max_fare=('fare_amount', 'max'),
        avg_fare=('fare_amount', 'mean'),
        services=('year_week', 'count')
    ).reset_index()

    # Calculamos la variación porcentual
    agregado_semanal_df['service_variation'] = round(agregado_semanal_df['services'].pct_change().abs().fillna(0) * 100, 2).astype(str) + '%'

    # Escribimos el .csv
    agregado_semanal_df.to_csv('../output/agregadoSemanal.csv', sep='|', index=False)


def generar_informe_mensual(data):
# Escribe los resultados en un archivo Excel con tres pestañas

    dataJFK = getJFKData(data)
    dataRegular = getRegularData(data)
    dataOther = getOtherData(data)

    with pd.ExcelWriter('../output/agregadoMensual.xlsx') as writer:
        dataJFK.to_excel(writer, sheet_name='JFK', index=False)
        dataRegular.to_excel(writer, sheet_name='Regular', index=False)
        dataOther.to_excel(writer, sheet_name='Others', index=False)

