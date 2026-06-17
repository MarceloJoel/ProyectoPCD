# 🚗 Proyecto de Ciencia de Datos: Mercado de Vehículos Usados

Análisis exploratorio de datos (EDA) y aplicación interactiva con **Streamlit** para visualizar el mercado de vehículos usados, identificando patrones de precios, kilometraje y características técnicas.

## 👥 Integrantes

| Nombre | Apellido |
|---|---|

| Marcelo | Rodriguez Cabrera |

---

## 📂 Estructura del proyecto

```
proyecto/
├── car_data.csv          # Dataset principal (Kaggle · CarDekho)
├── proyectoX.py          # Aplicación Streamlit
├── carros_proyecto.ipynb # Pipeline EDA completo (Jupyter)
└── README.md
```

---

## 📊 Dataset

| Propiedad | Detalle |
|---|---|
| Fuente | [Kaggle – Car Details v3](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho) |
| Filas | 8 128 |
| Columnas | 13 (12 tras eliminar `torque`) |
| Variables clave | `selling_price`, `km_driven`, `fuel`, `transmission`, `year`, `owner` |

---

## 🛠️ Requisitos e Instalación

Se requiere **Python 3.8+**. Instala las dependencias ejecutando:

```bash
pip install streamlit pandas matplotlib seaborn
```

> En sistemas donde `pip` apunta a Python 2, usa `pip3` o `python -m pip`.

---

## ▶️ Ejecución

1. Coloca el archivo `car_data.csv` en el mismo directorio que `proyectoX.py`.
2. Ejecuta la aplicación:

```bash
streamlit run proyectoX.py
```

3. El navegador se abrirá automáticamente en `http://localhost:8501`.

---

## 🗂️ Pipeline de análisis (Notebook)

El archivo `carros_proyecto.ipynb` documenta el proceso completo en 5 etapas:

| Etapa | Contenido |
|---|---|
| 1 – Obtención | Descarga y justificación del dataset |
| 2 – Carga y procesamiento | Limpieza de columnas con unidades (`mileage`, `engine`, `max_power`), imputación de nulos, eliminación de `torque` |
| 3 – EDA | Estadísticas descriptivas, distribuciones, detección de outliers |
| 4 – Consultas y transformaciones | Filtros, agrupaciones, columnas derivadas (`antiguedad`, `antiguedad_cat`, `precio_por_antiguedad`) |
| 5 – Visualización | Histogramas, scatter plots, boxplots, gráficos circulares y de líneas |

---

## 📱 Funcionalidades del Dashboard

- **Página principal** con descripción del proyecto e integrantes.
- **Carga automática** de datos con caché (`@st.cache_data`).
- **Filtros interactivos** por marca, combustible, transmisión, rango de año y precio máximo.
- **5 KPIs** actualizados en tiempo real según los filtros.
- **7 gráficos** (histograma, scatter, líneas, barras, boxplot, pie, ranking de marcas).
- **Tabla de datos** configurable con estadísticas descriptivas expandibles.
- **Conclusiones** derivadas del análisis exploratorio.

---

## 📝 Conclusiones Principales

1. **Kilometraje y precio** tienen una correlación negativa clara.
2. El **año de fabricación** es el principal determinante del valor del vehículo.
3. **Diesel y gasolina** dominan el mercado; los vehículos alternativos son marginales.
4. La **transmisión automática** genera una prima de precio sobre la manual.
5. El mercado está dominado por **vendedores particulares** (Individual).
6. Existen **outliers de alta gama** (Land Rover, Mercedes-Benz) que sesgan las distribuciones.
