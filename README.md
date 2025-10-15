# 👨‍👩‍👧 Separador de Nombres y Apellidos (Streamlit App)

Esta aplicación en Python, construida con Streamlit y Pandas, resuelve el problema común de dividir nombres completos contenidos en una columna de un archivo Excel, separándolos en sus componentes: nombres y apellidos. Está diseñada específicamente para manejar nombres complejos y vocablos.

## ✨ Características Principales

  * **Interfaz Gráfica Sencilla:** Desarrollado con Streamlit para una experiencia de usuario intuitiva (cargar, procesar y descargar).
  * **Manejo de Vocablos:** Lógica especial para agrupar preposiciones y artículos comunes (ej. `de`, `la`, `del`) con el apellido que le sigue.
  * **Separación Inteligente:** Asume que los **dos últimos componentes** de un nombre completo son el Primer Apellido y el Segundo Apellido (con manejo de excepciones para nombres cortos).
  * **Preservación de Datos:** El script solo modifica la columna de nombres; el resto de las columnas del archivo original se mantienen en su posición.
  * **Exportación Directa:** Permite la descarga del archivo Excel resultante directamente desde la interfaz.

## 🚀 Requisitos y Uso

### 1\. Requisitos

Asegúrate de tener Python 3.x instalado. Luego, instala las librerías necesarias:

```bash
pip install streamlit pandas openpyxl xlsxwriter
```

### 2\. Ejecución

Guarda el código como, por ejemplo, `app_separador.py`. Ejecuta la aplicación desde la terminal:

```bash
streamlit run app_separador.py
```

La aplicación se abrirá automáticamente en tu navegador web.

### 3\. Formato del Archivo de Entrada

El archivo Excel que subas **debe contener obligatoriamente** una columna llamada:

| Columna Requerida |
| :--- |
| `NOMBRE_COMPLETO` |

## 📐 Lógica de Procesamiento

El corazón del script es la función `procesar_nombres_apellidos(df)`, que aplica la siguiente lógica:

1.  **Normalización:** El nombre completo se convierte a minúsculas y se divide por espacios.
2.  **Agrupación de Vocablos:** Los vocablos definidos (`de`, `la`, `los`, `del`, `da`) se anexan a la siguiente palabra.
      * *Ejemplo:* "Juan **De La** Cruz" se convierte en tres componentes: `['juan', 'de la cruz']` (Si Juan fuera un nombre compuesto, el caso se gestiona también).
3.  **Asignación de Apellidos:** Se aplica la regla general para la asignación:
      * **Primer Apellido:** El penúltimo componente de la lista final de palabras.
      * **Segundo Apellido:** El último componente de la lista final de palabras.
      * Los componentes restantes se asignan como `Primer Nombre`, `Segundo Nombre`, etc.
4.  **Casos Especiales:** Se manejan excepciones como nombres con solo 2 o 3 palabras para asegurar una separación lógica.
5.  **Formato de Salida:** Las nuevas columnas se insertan en la posición original de la columna `NOMBRE_COMPLETO` y se aplica el formato de título (primera letra en mayúscula) a cada componente.

| Columnas de Salida Generadas |
| :--- |
| `Primer Nombre` |
| `Segundo Nombre` |
| `Tercer Nombre` |
| `Primer Apellido` |
| `Segundo Apellido` |
