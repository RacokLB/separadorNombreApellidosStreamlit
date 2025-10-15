# Estrategia de Trading con Patrones de Velas y Crossover de EMAs

Este proyecto implementa y somete a **Backtesting** una estrategia de trading algorítmico, diseñada según las especificaciones de un cliente, la cual combina la identificación de patrones específicos de velas japonesas con un filtro de cruce de Medias Móviles Exponenciales (EMAs).

**Conclusión Principal del Análisis:** Los resultados del Backtest demuestran que la estrategia, tal como fue definida, **no es rentable** en las condiciones de mercado probadas. Este repositorio sirve como documentación y prueba de concepto del análisis realizado.

## 🚀 Instalación y Requisitos

Para ejecutar el script y replicar el backtest, necesitarás Python 3.x y las siguientes librerías:

```bash
pip install MetaTrader5 pandas numpy backtesting pandas-ta matplotlib
```

### Requisitos Adicionales

1.  **MetaTrader 5 (MT5):** Debes tener instalado el terminal MT5 en la ruta especificada en el script.
2.  **Cuenta Demo MT5:** Se requiere una cuenta demo activa para la descarga de datos históricos.
      * **Configuración en el Script:** Asegúrate de actualizar las variables `MT5_PATH`, `MT5_ACCOUNT_LOGIN`, `MT5_ACCOUNT_PASSWORD` y `MT5_ACCOUNT_SERVER` con tus credenciales.

## ⚙️ Estructura y Funcionamiento del Script

El script se divide en tres componentes principales:

### 1\. Conexión y Descarga de Datos (`MetaTrader5`)

Las funciones iniciales se encargan de:

  * Conectar y autorizar la cuenta MT5.
  * Obtener información del símbolo (ej. tamaño del pip).
  * Descargar datos históricos (`copy_rates_range`) en formato de DataFrame de pandas, esencial para el backtest.

### 2\. Lógica de Patrones de Velas

El script define una serie de funciones booleanas (ej. `is_bullish_candle`, `is_hammer_like_bearish`, `is_bullish_engulfing`) que implementan la lógica del cliente para identificar las condiciones específicas del mercado:

  * **Señal de Compra (Long):** Busca una combinación de vela alcista (C3), patrón de martillo o similar (C2), y un patrón **envolvente alcista** (C1).
  * **Señal de Venta (Short):** Busca una combinación de vela bajista (C3), vela alcista con mecha superior mínima (C2), y un patrón **envolvente bajista** (C1).

### 3\. La Estrategia de Backtesting (`MyCandlestickStrategy`)

La clase `MyCandlestickStrategy` de `backtesting.py` encapsula la lógica operativa:

  * **Indicadores:** Implementa un filtro de **Cruce de EMAs (10 y 20 periodos)** usando `pandas_ta`. La señal de vela solo se ejecuta si se cumple la condición de cruce a favor de la dirección.
  * **Gestión de Posición:** Incluye una lógica de **Break-Even (Punto de Equilibrio)** que ajusta el Stop Loss al precio de entrada más un pequeño *offset* (`breakeven_pips_offset`) una vez que el beneficio flotante alcanza un umbral (`breakeven_pips_trigger`).
  * **Gestión de Riesgo:** Aplica un Stop Loss máximo (`max_sl_pips`) y una relación de Riesgo/Recompensa fija (`tp_factor = 1.2`).

## 📊 Ejecución del Backtest

La función `run_backtest_strategy()` configura y ejecuta el backtest:

| Parámetro | Valor Predeterminado | Descripción |
| :--- | :--- | :--- |
| **Símbolo** | `EURUSD` | Instrumento financiero a probar. |
| **Timeframe** | `M15` (15 minutos) | Periodicidad de las velas. |
| **Período** | 2023-01-01 a 2024-12-31 | Rango de fechas para el análisis. |
| **Capital Inicial** | `$10,000` | Capital ficticio para el backtest. |
| **Comisión** | `0.02%` | Comisión por operación. |

Para iniciar el análisis, simplemente ejecuta el script:

```bash
python nombre_del_script.py
```

Al finalizar, se imprimirá un resumen de estadísticas en la consola y se generará un archivo HTML interactivo (`EURUSD_15_backtest.html`) con la visualización del capital y las operaciones.

-----

## 🛑 Conclusión del Cliente

El análisis de la estrategia de trading del cliente (combinando los patrones específicos de velas con el filtro de cruce de EMA) arroja resultados consistentemente **negativos**. Esto confirma que, bajo los parámetros definidos, la estrategia no es viable para la operación en vivo y debe ser revisada o descartada.
