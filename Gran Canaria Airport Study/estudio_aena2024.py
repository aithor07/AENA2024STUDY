import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



aena_data = pd.read_csv("datos_limpios/aena_2024_limpio.csv")

# Limpiamos espacios en blanco ocultos al inicio o final de los nombres
aena_data['aeropuerto'] = aena_data['aeropuerto'].str.strip()


"""
IMPORTANTE: El CSV proporcionado por AENA no solo contiene informacion acerca de aeropuertos españoles,
tambien encontramos aeropuertos extranjeros como el de Saõ Paulo. Por lo que deberemos aplicar un filtrado
para descartar todo aeropuerto que no sea español.
"""



lista_exclusion_extranjeros = [
    "SÃO PAULO/CONGONHAS",
    "SÃO PAULO/CAMPO DE MARTE",
    "RIO DE JANEIRO/JACAREPAGUÁ",
    "RIO DE JANEIRO/SANTOS DUMONT",
    "UBERLÂNDIA",
    "UBERABA",
    "BELÉM/JÚLIO C. RIBEIRO",
    "BELÉM/VAL DE CANS",
    "MACAPÁ",
    "ALTAMIRA",
    "PARAUAPEBAS/CARAJÀS", 
    "MARABÀ",
    "PONTA PORÃ",
    "CORUMBÁ",
    "JOÃO PESSOA",
    "ARACAJU",
    "JUAZEIRO DO NORTE",
    "CAMPINA GRANDE",
    "LONDRES-LUTON",
    "RECIFE",
    "MONTES CLAROS",
    "MACEIÓ",
    "CARAJÀS",

]


df_sin_totales = aena_data[~aena_data["aeropuerto"].str.contains(
    "Total", 
    case=False, 
    na=False
)]

df_españa = df_sin_totales[~df_sin_totales["aeropuerto"].isin(lista_exclusion_extranjeros)].copy()

"""
Columnas de el CSV
---------------------------------------------------------------------------------
Index(['aeropuerto', 'pasajeros_total', 'pasajeros_inc_2023',
       'pasajeros_inc_2019', 'operaciones_total', 'operaciones_inc_2023',
       'operaciones_inc_2019', 'mercancia_total', 'mercancia_inc_2023',
       'mercancia_inc_2019'],
      dtype='object')
"""


#Cuales son los aeropuertos con más pasajeros de 2024, usando groupby()
#airports_most_passengers = df_españa.groupby("aeropuerto").pasajeros_total.max().sort_values(ascending=False)

#Otra manera (mas directa y preferible)
airports_most_passengers = df_españa.sort_values(by="pasajeros_total", ascending=False)

#Los aeropuertos con menos pasajeros
airports_least_passengers = df_españa.sort_values(by="pasajeros_total", ascending=True)
#--------------------------------------------------------------------------------------------------------

#Como se compara Gran Canaria con Tenerife sur en pasajeros?
gc_airport = df_españa[df_españa["aeropuerto"] == "GRAN CANARIA"]

tf_sur_airport = df_españa[df_españa["aeropuerto"] == "TENERIFE SUR"]

numero_pasajeros_gc = gc_airport.pasajeros_total.item()
numero_pasajeros_tf_sur = tf_sur_airport.pasajeros_total.item()

if (numero_pasajeros_gc > numero_pasajeros_tf_sur):
    print("Gran Canaria tuvo mas pasajeros en 2024 que Tenerife Sur con: " , numero_pasajeros_gc , " pasajeros.")
else:
    print("Tenerife Sur tuvo mas pasajeros que Gran Canaria en 2024 con: " , numero_pasajeros_tf_sur , " pasajeros.")
diferencia_gc_tf_sur = abs(numero_pasajeros_gc - numero_pasajeros_tf_sur)
print("La diferencia de pasajeros fue de " , diferencia_gc_tf_sur , " pasajeros.")
#-----------------------------------------------------------------------------------------------------------------------
#Top 10 aeropuertos top en cuanto a numero de visitantes en una gráfica de barras

#Solo queremos los aeropuertos de sitios, no totales o por el estilo por lo que primero filtramos
#El operador (~) -> Alt GR + 4 sirve para invertir una condicion por lo que ya podemos filtrar
data_filtrada = airports_most_passengers[~airports_most_passengers["aeropuerto"].str.contains("Total", case = False, na = False)]
top_10_data = data_filtrada.head(10)



#DEBUG
print("\n--- DEBUG: DATOS FINALES PARA EL GRÁFICO ---")
print(top_10_data[['aeropuerto', 'pasajeros_total']])

#Ajustamos tamaño del grafico
plt.figure(figsize=(10,7))
#Creamos grafico
grafico = sns.barplot(data=top_10_data, x="pasajeros_total", y="aeropuerto")
#Titulo del grafico
plt.title("Top 10 Aeropuertos por pasajeros España 2024")
#Etiqueta eje x
plt.xlabel("Total Pasajeros (Millones)")
#Etiqueta eje y
plt.ylabel("Aeropuerto")
#Ajusta automaticamente el grafico
plt.tight_layout()
#Mostrar el grafico
plt.show()





#Vamos a obtener mas valor de estos datos respondiendo varias preguntas
#Cuales son los aeropuertos 'revelacion' , es decir, mejor recuperacion post-pandemia
aeropuertos_revelacion = df_españa.sort_values(by="pasajeros_inc_2019", ascending=False)
aeropuerto_pasajeros2019 = aeropuertos_revelacion[["aeropuerto", "pasajeros_inc_2019"]]
print("AEROPUERTOS CON MEJOR RECUPERACION POST PANDEMIA")
print(aeropuerto_pasajeros2019.head(10))

sns.catplot(data=aeropuerto_pasajeros2019.head(10), x="aeropuerto", y="pasajeros_inc_2019")
plt.xlabel("Aeropuerto")
plt.ylabel("Incremento 2019 (Pandemia) - 2024 (%)")
plt.tight_layout()
plt.title("Aeropuertos con mayor incremento Pandemia-2024")
plt.show()


#Que aeropuertos de Canarias son los mas importantes en base a pasajeros totales
aeropuertos_canarias = [
    "GRAN CANARIA",

    "TENERIFE SUR",

    "LANZAROTE CÉSAR MANRIQUE",

    "TENERIFE NORTE-C. LA LAGUNA",

    "FUERTEVENTURA",

    "LA PALMA",

    "EL HIERRO",

    "LA GOMERA"
]

aeropuertos_canarios = df_españa[df_españa["aeropuerto"].isin(aeropuertos_canarias)].sort_values(by="pasajeros_total", ascending=False)
sns.barplot(data=aeropuertos_canarios, x="aeropuerto", y="pasajeros_total")
plt.xlabel("Aeropuerto Canario")
plt.ylabel("Pasajeros Totales 2024")
plt.tight_layout()
plt.title("Aeropuertos Canarios por Cantidad de Pasajeros Totales")
plt.show()
#-----------------------------------------------------------------------------------------------------------------------------------------------
#Que aeropuertos de España son los mas eficientes (pasajeros_totales/operaciones_totales)
#¿Son los aeropuertos más grandes (más pasajeros) también los más eficientes (más pasajeros por vuelo)?
df_españa["pasajeros_por_vuelo"] = df_españa["pasajeros_total"] / df_españa["operaciones_total"]
aeropuerto_eficiencia = df_españa.sort_values(by="pasajeros_por_vuelo", ascending=False)
aeropuerto_eficiencia_filtrado = aeropuerto_eficiencia[["aeropuerto", "pasajeros_por_vuelo"]]
sns.scatterplot(data=df_españa, x="pasajeros_total", y="pasajeros_por_vuelo")
plt.title("Eficiencia vs. Tamaño de Aeropuertos Españoles (2024)", fontsize=16)
plt.xlabel("Total Pasajeros (Tamaño)", fontsize=12)
plt.ylabel("Pasajeros por Vuelo (Eficiencia)", fontsize=12)
plt.tight_layout()
plt.show()
#-------------------------------------------------------------------------------------------------------------------------
#Hay correlacion entre pasajeros y mercancia?

top_pasajeros = df_españa.nlargest(10, "pasajeros_total")
top_mercancia = df_españa.nlargest(10, "mercancia_total")
top_interesantes = pd.concat([top_pasajeros, top_mercancia]).drop_duplicates()
top_interesantes = top_interesantes.sort_values(by="pasajeros_total", ascending=False)


plt.figure(figsize=(14,8))

bubble_chart = sns.scatterplot(
    data=top_interesantes,
    x="aeropuerto",
    y="pasajeros_total",
    size="mercancia_total",
    sizes=(50, 2000),
    hue="mercancia_total",
    palette="viridis"
)
# Rotar las etiquetas del eje X para que sean legibles
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylabel("Pasajeros Totales")
plt.xlabel("Aeropuertos")

# Mover la leyenda (la guía de tamaños)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

plt.title("Relacion Pasajeros y Mercancia")

plt.tight_layout()
plt.show()




