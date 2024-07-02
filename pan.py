import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Conexión a la base de datos en localhost
engine = create_engine('mysql+mysqldb://root:@localhost/conteo')

# Consulta SQL para verificar si hay datos en la tabla
query = "SELECT COUNT(*) FROM car_counts"
df_count = pd.read_sql(query, engine)

# Imprimir la cantidad de filas en la tabla
print("Número de filas en la tabla 'car_counts':", df_count.iloc[0, 0])

# Consulta SQL para obtener los datos
query = "SELECT timestamp, count FROM car_counts"
df = pd.read_sql(query, engine)

# Asegurarse de que los datos sean correctos
print("Primeras filas del conjunto de datos:")
pd.set_option('display.max_rows', None)  # Mostrar todas las filas
print(df.head(50))  # Mostrar las primeras 50 filas del DataFrame

if df.empty:
    print("El DataFrame está vacío. Verifica la consulta SQL y la base de datos.")
else:
    # Crear una columna 'day_of_week' a partir de 'timestamp'
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['day_of_week'] = df['timestamp'].dt.dayofweek + 1  # +1 para que el lunes sea 1 y domingo sea 7

    # Convertir los valores de 'day_of_week' a cadenas con el prefijo "Dia"
    df['day_of_week'] = df['day_of_week'].apply(lambda x: f"Dia {x}")

    # Extraer la hora de 'timestamp'
    df['time'] = df['timestamp'].dt.strftime('%H:%M')

    # Variables independientes y dependientes
    X = df[['time', 'day_of_week']]
    X = pd.get_dummies(X, columns=['time', 'day_of_week'], drop_first=True)  # Codificación one-hot para las columnas 'time' y 'day_of_week'
    y = df['count']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predecir y evaluar
    y_pred = model.predict(X_test)
    print("Predicciones:", y_pred[:100])
    print("Precisión del modelo:", model.score(X_test, y_test))


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
