import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Conexión a la base de datos y carga de datos
engine = create_engine('mysql+mysqldb://root:@localhost/conteo')
table_name = 'car_counts'
query = f"SELECT * FROM {table_name}"
df = pd.read_sql(query, con=engine)

# Imprimir las primeras filas del DataFrame para verificar las columnas
print(df.head())

# Preprocesamiento de los datos
if 'dia' in df.columns and 'hora' in df.columns:
    df['dia'] = df['dia'].astype(str)  # Convertir a string
    df['hora'] = df['hora'].astype(str)  # Convertir a string
    df['datetime'] = pd.to_datetime(df['dia'] + ' ' + df['hora'], errors='coerce')  # Crear datetime
    df.set_index('datetime', inplace=True)
    df = df[['carros']]

    # Escalado de los datos
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df)

    # Función para crear la estructura de datos de la LSTM
    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-time_step-1):
            a = dataset[i:(i+time_step), 0]
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    # Parámetros
    time_step = 10

    # Creación del conjunto de datos de entrenamiento y prueba
    train_size = int(len(scaled_data) * 0.8)
    test_size = len(scaled_data) - train_size
    train_data, test_data = scaled_data[0:train_size, :], scaled_data[train_size:len(scaled_data), :]

    # Creación del dataset para la LSTM
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    # Redimensionar los datos para la LSTM [samples, time steps, features]
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Crear el modelo LSTM
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compilar el modelo
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Entrenar el modelo
    model.fit(X_train, y_train, batch_size=1, epochs=1)

    # Guardar el modelo entrenado
    model.save('modelo_lstm.h5')

    # Hacer predicciones
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    # Invertir el escalado de las predicciones
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    y_train = scaler.inverse_transform([y_train])
    y_test = scaler.inverse_transform([y_test])

    # Calcular el RMSE
    train_rmse = np.sqrt(np.mean(((train_predict - y_train[0]) ** 2)))
    test_rmse = np.sqrt(np.mean(((test_predict - y_test[0]) ** 2)))
    print(f'Train RMSE: {train_rmse}')
    print(f'Test RMSE: {test_rmse}')

    # Imprimir predicciones
    print("Predicciones del conjunto de entrenamiento:")
    print(train_predict[:100])  # Muestra los primeros 20 resultados de las predicciones del conjunto de entrenamiento

    print("Predicciones del conjunto de prueba:")
    print(test_predict[:24])  # Muestra los primeros 20 resultados de las predicciones del conjunto de prueba

    # Graficar los resultados
    train_plot = np.empty_like(scaled_data)
    train_plot[:, :] = np.nan
    train_plot[time_step:len(train_predict)+time_step, :] = train_predict

    test_plot = np.empty_like(scaled_data)
    test_plot[:, :] = np.nan
    test_plot[len(train_predict)+(time_step*2)+1:len(scaled_data)-1, :] = test_predict

    plt.plot(scaler.inverse_transform(scaled_data), label='Real data')
    plt.plot(train_plot, label='Train predictions')
    plt.plot(test_plot, label='Test predictions')
    plt.legend()
    plt.show()

    # Insertar predicciones en la tabla 'pronostico'
    predicciones = np.concatenate((train_predict, test_predict))
    fechas = df.index[time_step:time_step + len(predicciones)]

    data_to_insert = pd.DataFrame({'fecha': fechas.date, 'hora': fechas.time, 'prediccion': np.round(predicciones.flatten())})
    data_to_insert['id'] = np.arange(1, len(data_to_insert) + 1)
    data_to_insert = data_to_insert[['id', 'fecha', 'hora', 'prediccion']]

    data_to_insert.to_sql('pronostico', con=engine, if_exists='append', index=False)

else:
    print("Las columnas 'dia' y/o 'hora' no existen en el DataFrame.")


#engine = create_engine('mysql+mysqldb://Pesheto:pesheto69@34.151.233.27/Grupo1')

# np.random.seed(42)
# num_minutes_per_hour = 60
# num_hours = 10
# num_samples = num_hours * num_minutes_per_hour
# hours = np.repeat(np.arange(10, 20), num_minutes_per_hour)
# minutes = np.tile(np.arange(num_minutes_per_hour), num_hours)
# days_of_week = np.random.randint(1, 2, num_samples)  # Cambiar los días a solo "Dia 1"
# vehicle_counts = np.random.poisson(lam=20, size=num_samples) + (hours - 12)**2 / 10 + (days_of_week - 3)**2 / 2

# # Crear una columna de tiempo en formato HH:MM
# time = [f"{hour:02d}:{minute:02d}" for hour, minute in zip(hours, minutes)]

# # Convertir los valores de 'day_of_week' a cadenas con el prefijo "dia"
# days_of_week_str = [f"Dia {day}" for day in days_of_week]

# df = pd.DataFrame({
#     'time': time,
#     'day_of_week': days_of_week_str,
#     'conteo': vehicle_counts
# })
# pd.set_option('display.max_rows', None)  # Mostrar todas las filas
# print("Primeras filas del conjunto de datos:")
# print(df.head(721))

# # Variables independientes y dependientes
# X = df[['time', 'day_of_week']]
# X = pd.get_dummies(X, columns=['time', 'day_of_week'], drop_first=True)  # Codificación one-hot para las columnas 'time' y 'day_of_week'
# y = df['conteo']

# # Dividir los datos en conjuntos de entrenamiento y prueba
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Entrenar el modelo
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Predecir y evaluar
# y_pred = model.predict(X_test)
# print("Predicciones:", y_pred[:50])
# print("Precisión del modelo:", model.score(X_test, y_test))
