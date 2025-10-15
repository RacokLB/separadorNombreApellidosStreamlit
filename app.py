import streamlit as st
import pandas as pd
from io import BytesIO
import xlsxwriter 

# --- Función de Procesamiento ---
def procesar_nombres_apellidos(df):
    """
    Procesa un DataFrame separando nombres/apellidos y mantiene todas
    las otras columnas en su posición original.
    """
    nombres_completos = 'NOMBRE_COMPLETO'

    # Validamos que la columna 'NOMBRE_COMPLETO' exista antes de continuar
    if nombres_completos not in df.columns:
        st.error(f"Error: El archivo debe contener una columna llamada '{nombres_completos}' para poder procesar.")
        return None

    # 1. Definición de las nuevas columnas de salida.
    columnas_separadas = [
        'Primer Nombre', 'Segundo Nombre', 'Tercer Nombre',
        'Primer Apellido', 'Segundo Apellido'
    ]
    # Se crea una lista de diccionarios para recopilar las nuevas columnas
    filas_procesadas = []

    # Lista de vocablos a anexar
    vocablos_a_anexar = {'de', 'la', 'los', 'del', 'da'}

    # Creacion st.progress para mostrar el avance al usuario (UI)
    total_filas = len(df)
    progress_bar = st.progress(0)
    estado_texto = st.empty()

    for index, row in df.iterrows():
        # Actualizar la barra de progreso
        porcentaje_completado = (index + 1) / total_filas
        progress_bar.progress(porcentaje_completado)
        estado_texto.text(f"Procesando fila {index + 1} de {total_filas}...")

        nombre_completo = str(row[nombres_completos]).lower()
        
        palabras_originales = nombre_completo.split()

        # --- LÓGICA DE ANEXIÓN MEJORADA  ---
        palabras_agrupadas = []
        i = 0
        while i < len(palabras_originales):
            cadena_vocablos = []
            while i < len(palabras_originales) and palabras_originales[i] in vocablos_a_anexar:
                cadena_vocablos.append(palabras_originales[i])
                i += 1
            if i < len(palabras_originales):
                palabra_principal = palabras_originales[i]
                i += 1
                if cadena_vocablos:
                    palabra_final = " ".join(cadena_vocablos) + " " + palabra_principal
                    palabras_agrupadas.append(palabra_final)
                else:
                    palabras_agrupadas.append(palabra_principal)
            elif cadena_vocablos:
                palabras_agrupadas.extend(cadena_vocablos)
        # --- FIN LÓGICA DE ANEXIÓN ---

        palabras = palabras_agrupadas
        num_palabras = len(palabras) # CONTEO CLAVE

        # --- LÓGICA CORREGIDA PARA MANEJAR NOMBRES/APELLIDOS (dentro del bucle) ---
        
        # Inicialización segura
        nombres = []
        apellidos = []

        if num_palabras <= 1:
            # Caso: Solo Nombre o Vacío
            nombres = [palabras] # Si es vacío, queda [], si es 1 palabra, queda [Palabra]
            apellidos = ['', ''] # Asegura tener 2 elementos para evitar errores de índice
        elif num_palabras == 2:
            # CASO EXCEPCIÓN: UN NOMBRE y UN APELLIDO (Ej. Juan Perez)
            nombres = [palabras[0]] # Primer elemento es el nombre
            apellidos = [palabras[1], ''] # Segundo elemento es el Primer Apellido, Segundo vacío
        elif num_palabras == 3:
            #CASO DE EXCEPCION : 2 NOMBRES Y UN APELLIDO (Ej. Carlos Alberto Gomez)
            nombres = [palabras[0],palabras[1]] #Primer y segundo elemento son los nombres
            apellidos =[palabras[2]]
        else: # num_palabras >= 3
            # Caso estándar: (Nombre1 [Nombre2...]) Apellido1 Apellido2
            # Se asume que los dos últimos elementos son los apellidos
            apellidos = palabras[-2:]
            nombres = palabras[:-2]
            
        # --- FIN LÓGICA ---
        
        # Preparamos los datos de la fila (USANDO LA LISTA DE NOMBRES Y APELLIDOS RESULTANTES)
        fila_datos = {
            # Asegura el uso de .title() y maneja el índice si la lista está vacía/corta
            'Primer Nombre': nombres[0].title() if len(nombres) > 0 else '',
            'Segundo Nombre': nombres[1].title() if len(nombres) > 1 else '',
            'Tercer Nombre': nombres[2].title() if len(nombres) > 2 else '',
            'Primer Apellido': apellidos[0].title() if len(apellidos) > 0 else '',
            'Segundo Apellido': apellidos[1].title() if len(apellidos) > 1 else ''
        }
        filas_procesadas.append(fila_datos)
    
    # Limpiar el progreso
    progress_bar.empty()
    estado_texto.empty()

    # 3. Concatenamos todas las filas procesadas en un DataFrame
    df_separado = pd.DataFrame(filas_procesadas, columns=columnas_separadas)

    # --- PASOS PARA LA UNIÓN ---
    columna_a_reemplazar = nombres_completos
    posicion_insercion = df.columns.get_loc(columna_a_reemplazar)

    # 5. Eliminamos la columna original que se acaba de procesar.
    df_resultado = df.drop(columns=[columna_a_reemplazar])

    # 6. Inserta el nuevo DataFrame separado en la posición de la columna eliminada.
    for i, col_name in enumerate(columnas_separadas):
        df_resultado.insert(posicion_insercion + i, col_name, df_separado[col_name])

    return df_resultado

# --- Función para crear un archivo Excel en memoria para la descarga ---
@st.cache_data
def convertir_a_excel(df):
    """Convierte el DataFrame a un objeto BytesIO (buffer) para descarga."""
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Nombres_Separados')
    writer.close()
    processed_data = output.getvalue()
    return processed_data


# =====================================================================
#                          INTERFAZ STREAMLIT
# =====================================================================

st.set_page_config(
    page_title="Separador de Nombres y Apellidos",
    layout="centered"
)

st.title("👨‍👩‍👧 Separador de Nombres y Apellidos")
st.markdown("""
Sube un archivo **Excel (.xlsx)**. La aplicación procesará la columna
llamada **`NOMBRE_COMPLETO`** y separará los nombres y apellidos en nuevas columnas,
manteniendo el resto de tu data intacta.
""")

# --- Entrada de archivo (El alma de la UI) ---
uploaded_file = st.file_uploader(
    "1. Carga tu archivo Excel aquí:", 
    type=['xlsx']
)

if uploaded_file is not None:
    try:
        # Leer el archivo que subió el usuario en Streamlit
        df_original = pd.read_excel(uploaded_file)
        
        st.success("Archivo cargado correctamente. Listo para procesar.")
        st.dataframe(df_original.head())

        # --- Botón de Ejecución ---
        if st.button("2. Procesar Nombres y Apellidos", type="primary"):
            st.warning("Procesando datos... ¡por favor, espera!")
            
            # Llamar a la función de procesamiento con el DataFrame
            df_final = procesar_nombres_apellidos(df_original.copy())

            if df_final is not None:
                st.success("✅ ¡Procesamiento finalizado con éxito!")
                st.subheader("Vista Previa del Resultado")
                st.dataframe(df_final.head(10)) # Muestra las primeras 10 filas

                # --- Botón de Descarga ---
                excel_data = convertir_a_excel(df_final)
                
                st.download_button(
                    label="3. Descargar Archivo Procesado (.xlsx)",
                    data=excel_data,
                    file_name='data_procesada_streamlit.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    help="Haz clic para descargar el nuevo archivo Excel con las columnas separadas."
                )
                st.balloons()
            
    except Exception as e:
        # Captura cualquier error de lectura o procesamiento
        st.error(f"Ocurrió un error durante la carga o procesamiento: {e}")
