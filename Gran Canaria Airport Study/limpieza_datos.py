import pandas as pd
import numpy as np

# --- 1. Definir la Estructura (Columnas y Filas) ---

# Columnas de la tabla de PASAJEROS
cols_pasajeros = {
    'Aeropuertos': 'aeropuerto',
    'Total': 'pasajeros_total',
    '% Inc 2024 /s 2023': 'pasajeros_inc_2023',
    '% Inc 2024 /s 2019': 'pasajeros_inc_2019'
}

# Columnas de la tabla de OPERACIONES
cols_operaciones = {
    'Aeropuertos.1': 'aeropuerto',
    'Total.1': 'operaciones_total',
    '% Inc 2024 /s 2023.1': 'operaciones_inc_2023',
    '% Inc 2024 /s 2019.1': 'operaciones_inc_2019'
}

# Columnas de la tabla de MERCANCÍA
cols_mercancia = {
    'Aeropuertos.2': 'aeropuerto',
    'Total.2': 'mercancia_total',
    '% Inc 2024 /s 2023.2': 'mercancia_inc_2023',
    '% Inc 2024 /s 2019.2': 'mercancia_inc_2019'
}

# Filas que no queremos cargar (títulos, espacios en blanco)
filas_a_saltar = [0, 1, 2, 3, 4, 6]
nombre_archivo = "DEFINITIVOS+2024.xlsx - AÑO 2024.csv"

# --- 2. Cargar, Limpiar y Unir las 3 Tablas ---

# Cargar Pasajeros
df_pasajeros = pd.read_csv(
    nombre_archivo,
    usecols=cols_pasajeros.keys(),
    skiprows=filas_a_saltar
).rename(columns=cols_pasajeros)

# Cargar Operaciones
df_operaciones = pd.read_csv(
    nombre_archivo,
    usecols=cols_operaciones.keys(),
    skiprows=filas_a_saltar
).rename(columns=cols_operaciones)

# Cargar Mercancía
df_mercancia = pd.read_csv(
    nombre_archivo,
    usecols=cols_mercancia.keys(),
    skiprows=filas_a_saltar
).rename(columns=cols_mercancia)

# Limpiar filas vacías (NaN) que se cuelan al final
df_pasajeros = df_pasajeros.dropna(subset=['aeropuerto'])
df_operaciones = df_operaciones.dropna(subset=['aeropuerto'])
df_mercancia = df_mercancia.dropna(subset=['aeropuerto'])

# Unir las 3 tablas en un solo DataFrame
# how='outer' se asegura de no perder aeropuertos si faltan en alguna tabla
df_final = df_pasajeros.merge(
    df_operaciones, on='aeropuerto', how='outer'
).merge(
    df_mercancia, on='aeropuerto', how='outer'
)

# --- 3. Convertir Texto a Números ---

# Lista de columnas de totales (con puntos)
cols_totales = ['pasajeros_total', 'operaciones_total', 'mercancia_total']

# Lista de columnas de porcentajes (con '%' y ',')
cols_porcentaje = [
    'pasajeros_inc_2023', 'pasajeros_inc_2019',
    'operaciones_inc_2023', 'operaciones_inc_2019',
    'mercancia_inc_2023', 'mercancia_inc_2019'
]

# Bucle para limpiar columnas de TOTALES
for col in cols_totales:
    if col in df_final.columns:
        # 1. Asegurarnos de que es texto (str) y quitar los puntos ('.')
        df_final[col] = df_final[col].astype(str).str.replace('.', '', regex=False)
        
        # 2. Convertir a número. 
        # errors='coerce' pone NaN si algo falla (ej. una celda vacía)
        df_final[col] = pd.to_numeric(df_final[col], errors='coerce')

# Bucle para limpiar columnas de PORCENTAJES
for col in cols_porcentaje:
     if col in df_final.columns:
        # 1. Asegurarnos de que es texto (str)
        # 2. Quitar el signo de porcentaje ('%')
        # 3. Reemplazar la coma (',') por un punto ('.')
        df_final[col] = df_final[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
        
        # 2. Convertir a número (float)
        df_final[col] = pd.to_numeric(df_final[col], errors='coerce')

# --- 4. Ver el Resultado ---

print("--- DataFrame Limpio y Convertido ---")
df_final.info()

print("\n--- Fila de GRAN CANARIA ---")
print(df_final[df_final['aeropuerto'].str.contains('GRAN CANARIA', case=False, na=False)])

# Guardar el dataset limpio como CSV
df_final.to_csv("aena_2024_limpio.csv", index=False)