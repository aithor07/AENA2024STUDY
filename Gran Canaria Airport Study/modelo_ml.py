import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score




df_limpio = pd.read_csv("datos_limpios/aena_2024_limpio.csv")
df_limpio["aeropuerto"] = df_limpio["aeropuerto"].str.strip()



"""
Con los datos que he obtenido, seria posible predecir los pasajeros totales de un aeropuerto
en base al numero de operaciones totales que va a tener?

Por que esto es util:

Imaginemos que el aeropuerto de Gran Canaria anuncia que va a añadir 5.000 operaciones
nuevas el año que viene (operaciones = nuevas rutas). Mediante un modelo de machine learning podriamos
estimar cuantos pasajeros extra podria supone esto.
"""



#Definiremos las columnas que usaremos para 'adivinar' y la columna que queremos 'adivinar'
#Tambien limpiaremos los NaN
df_modelo = df_limpio.dropna(subset=["operaciones_total", "pasajeros_total"])
#Definimos X, que tiene que ser un dataframe, de ahi los dobles corchetes
X = df_modelo[["operaciones_total"]]
#Definimos y (la respuesta que buscamos)
y = df_modelo["pasajeros_total"]


#Dividiremos los datos de manera que el 80% seran para 'estudiar' y el 20% para probar, con respuestas que nunca vio.
#test_size = 0.2
#Semilla para que el resultado sea reproducible
#random_state = 42

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

#Creamos el modelo y lo entrenamos
#Creamos una calculadora de regresion lineal vacia
modelo = LinearRegression()
#Aprender la relacion entre X_train (operaciones) y y_train (pasajeros)
modelo.fit(X_train, y_train)
print("\n---Fin Entrenamiento---")

#Vamos a evaluar el modelo, en otras palabras, que nota ha sacado con sus predicciones comparandolas a datos reales
predicciones = modelo.predict(X_test)
#Comparamos
comparacion = pd.DataFrame({
    "Pasajeros Reales":y_test,
    "Pasajeros Predichos": predicciones
})
print("\n---Comparacion del Examen (Datos de Test)---")
print(comparacion.head())

#La nota final (R-cuadrado o R2)
#R2 nos dice que porcentaje de la variacion de pasajeros es capaz de explicar nuestro modelo
nota_r2 = r2_score(y_test, predicciones)
print(f"\nNota del Modelo (R2): {nota_r2 * 100:.2f}%")

"""
Como podemos observar la R2 del modelo es altisima, hace predicciones casi identicas a los datos reales,
demostrando que la relacion entre operaciones y pasajeros de los aeropuertos es extremadamente lineal y predecible.

Dicho esto, como le sacamos utilidad a este modelo?

Vamos a responder a la cuestion hipotetica planteada anteriormente, que ocurriria si a Gran Canaria se le añaden 5000 operaciones
nuevas, como afectaria esto al numero de pasajeros totales que pasan por el aeropuerto al año.
"""

#Vamos a volver a entrenar al modelo pero esta vez con todos los datos, ya que ya sabemos que es hiper preciso
modelo_final = LinearRegression()
modelo_final.fit(X, y) #Datos completos sin dividir
try:
    #Obtener datos actuales de Gran Canaria
    gc_actual = df_modelo[df_modelo["aeropuerto"] == "GRAN CANARIA"]

    if gc_actual.empty:
        print("Error: No se encontró Gran Canaria en los datos limpios.")
    else:
        ops_actuales_gc = gc_actual["operaciones_total"].item()
        pasajeros_actuales_gc = gc_actual["pasajeros_total"].item()

        #Escenario hipotetico
        operaciones_extra = 5000
        escenario_ops_gc = ops_actuales_gc + operaciones_extra

        #Predecimos
        prediccion = modelo_final.predict([[escenario_ops_gc]])
        #Pasajeros predichos (sacamos el numero del array)
        pasajeros_predichos = prediccion[0]
        #Pasajeros impacto/diferencia
        pasajeros_impacto = pasajeros_predichos - pasajeros_actuales_gc

        #Mostrar el resultado
        print(f"\n--- Simulación para GRAN CANARIA ---")
        print(f"Operaciones actuales:     {ops_actuales_gc:,.0f}")
        print(f"Pasajeros actuales:       {pasajeros_actuales_gc:,.0f}")
        print("------------------------------------------")
        print(f"Añadiendo {operaciones_extra:,.0f} operaciones...")
        print(f"Total operaciones nuevas: {escenario_ops_gc:,.0f}")
        print(f"Pasajeros PREDECIDOS:   {pasajeros_predichos:,.0f}")
        print(f"\nIMPACTO ESTIMADO (Pasajeros extra): +{pasajeros_impacto:,.0f}")
except Exception as e:
    print(f"Error durante la simulacion: {e}")
    print("Asegurate de que Gran Canaria esta en 'datos_limpios/aena_2024_limpio.csv'")
