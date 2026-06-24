import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ──────────────────────────────────────────────
# CONFIGURACIÓN PÁGINA DE STREAMLIT
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard · Vehículos Usados",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta coherente
COLOR_PRIMARY = "#7C3AED"
COLOR_SEC     = "#10B981"
COLOR_WARN    = "#F59E0B"
PALETTE       = "Set2"

# ──────────────────────────────────────────────
# 1. CARGA Y LIMPIEZA DE DATOS
# ──────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("car_data.csv")

    for col in ["mileage", "engine", "max_power"]:
        df[col] = df[col].astype(str).str.extract(r"(\d+\.?\d*)")
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    df["seats"] = df["seats"].fillna(df["seats"].median())
    df.drop(columns=["torque"], inplace=True, errors="ignore")

    df["brand"]              = df["name"].str.split().str[0]
    df["antiguedad"]         = 2026 - df["year"]
    df["precio_por_antiguedad"] = (df["selling_price"] / (df["antiguedad"] + 1)).round(3)
    

    return df

df = load_data()

# ──────────────────────────────────────────────
# 2. PÁGINA PRINCIPAL — DESCRIPCIÓN
# ──────────────────────────────────────────────
st.title(" Mercado de Vehículos Usados")
st.markdown(
    """
    **Dashboard interactivo** desarrollado como proyecto integrador para el curso
    *Programación para la Ciencia de Datos*.  
    El análisis se basa en el dataset [Car Details v3](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho)
    de Kaggle, que contiene **8 128 registros y 13 columnas**.
    """
)
st.divider()

# ──────────────────────────────────────────────
# 3. FILTROS EN SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filtros")

    with st.expander("🚗 Marca", expanded=True):
        marcas_disp = sorted(df["brand"].unique())
        marcas_sel  = st.multiselect(
            "Selecciona marca(s)",
            options=marcas_disp,
            default=marcas_disp[:5],
            help="Selecciona una o varias marcas.",
        )

    with st.expander("⚙️ Especificaciones", expanded=True):
        fuel_disp = sorted(df["fuel"].unique())
        fuel_sel  = st.multiselect(
            "Tipo de combustible",
            options=fuel_disp,
            default=fuel_disp,
        )

        trans_disp = sorted(df["transmission"].unique())
        trans_sel  = st.multiselect(
            "Transmisión",
            options=trans_disp,
            default=trans_disp,
        )

    with st.expander("💰 Rango de Año y Precio", expanded=True):
        yr_min, yr_max = int(df["year"].min()), int(df["year"].max())
        year_range = st.slider(
            "Rango de año",
            min_value=yr_min,
            max_value=yr_max,
            value=(2010, yr_max),
        )

        price_max = int(df["selling_price"].max())
        price_range = st.slider(
            "Precio máximo (₹)",
            min_value=0,
            max_value=price_max,
            value=price_max,
            step=50_000,
            format="₹%d",
        )

mask = (
    df["brand"].isin(marcas_sel)
    & df["fuel"].isin(fuel_sel)
    & df["transmission"].isin(trans_sel)
    & df["year"].between(*year_range)
    & (df["selling_price"] <= price_range)
)
dff = df[mask].copy()

if dff.empty:
    st.warning("Ningún registro coincide con los filtros seleccionados. Ajusta los parámetros.")
    st.stop()

# ──────────────────────────────────────────────
# 4. KPIs — INDICADORES PRINCIPALES
# ──────────────────────────────────────────────
st.subheader("INDICADORES PRINCIPALES")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total vehículos",    f"{len(dff):,}")
k2.metric("Precio promedio",    f"{dff['selling_price'].mean():,.0f}₹")
k3.metric("Precio mediano",     f"{dff['selling_price'].median():,.0f}₹")
k4.metric("Kilometraje promedio",  f"{dff['km_driven'].mean():,.0f} km")
k5.metric("Antigüedad promedio",   f"{dff['antiguedad'].mean():.1f} años")

st.divider()

# ──────────────────────────────────────────────
# 5. VISUALIZACIONES INTERACTIVAS
# ──────────────────────────────────────────────
st.subheader("ANÁLISIS VISUAL")

tab1, tab2, tab3 = st.tabs([
    "Análisis de Precios", 
    "Desempeño y Transmisión", 
    "Estructura del Mercado"
])

with tab1:
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("**Distribución del precio de venta**")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(dff["selling_price"], bins=40, kde=True, color=COLOR_PRIMARY, ax=ax)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e5:.0f}L"))
        ax.set_xlabel("Precio (Lakhs ₹)")
        ax.set_ylabel("Frecuencia")
        ax.set_title("")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.caption(
            "La mayoría de los vehículos se concentra en el segmento de precio bajo, "
            "con una distribución sesgada a la derecha que refleja pocos vehículos de gama alta."
        )

    with col_p2:
        st.markdown("**Evolución del precio promedio por año**")
        precio_anio = dff.groupby("year")["selling_price"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(precio_anio["year"], precio_anio["selling_price"], marker="o", color=COLOR_SEC, linewidth=2)
        ax.fill_between(precio_anio["year"], precio_anio["selling_price"], alpha=0.15, color=COLOR_SEC)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e5:.1f}L"))
        ax.set_xlabel("Año de fabricación")
        ax.set_ylabel("Precio promedio")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.caption("A mayor año de fabricación, mayor precio promedio: la antigüedad es el factor con mayor peso en la depreciación.")

    st.markdown("**Top 10 marcas por precio promedio**")
    top_brands = (
        dff.groupby("brand")["selling_price"]
        .agg(["mean", "count"])
        .query("count >= 10")
        .sort_values("mean", ascending=False)
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x=top_brands.index, y=top_brands["mean"], palette="bone", ax=ax)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e5:.1f}L"))
    ax.set_xlabel("Marca")
    ax.set_ylabel("Precio promedio")
    plt.xticks(rotation=30)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    st.caption("Marcas de lujo como Land Rover y Mercedes-Benz lideran el precio promedio; el volumen principal pertenece a Maruti y Hyundai.")

with tab2:
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("**Kilometraje vs. Precio por tipo de combustible**")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(
            x="km_driven", y="selling_price",
            hue="fuel", data=dff,
            palette=PALETTE, alpha=0.6, ax=ax,
        )
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e5:.0f}L"))
        ax.set_xlabel("Kilometraje (km)")
        ax.set_ylabel("Precio de venta")
        ax.legend(title="Combustible", fontsize=8)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.caption(
            "Correlación negativa: mayor kilometraje → menor precio. "
            "Los vehículos diésel suelen distribuirse en rangos de precio diferentes a los de gasolina."
        )

    with col_t2:
        st.markdown("**Precio de venta según transmisión**")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(x="transmission", y="selling_price", data=dff, palette=PALETTE, ax=ax)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e5:.0f}L"))
        ax.set_xlabel("Transmisión")
        ax.set_ylabel("Precio de venta")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.caption("Los automáticos alcanzan precios significativamente más altos, lo que los posiciona como bienes diferenciados.")

with tab3:
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.markdown("**Cantidad de vehículos por tipo de combustible**")
        fig, ax = plt.subplots(figsize=(6, 4))
        order = dff["fuel"].value_counts().index
        sns.countplot(x="fuel", data=dff, order=order, palette=PALETTE, ax=ax)
        ax.set_xlabel("Tipo de combustible")
        ax.set_ylabel("Cantidad")
        for p in ax.patches:
            ax.annotate(f"{int(p.get_height()):,}", (p.get_x() + p.get_width() / 2, p.get_height()),
                        ha="center", va="bottom", fontsize=9)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.caption("Diesel y gasolina dominan el mercado, con una presencia marginal de vehículos GNC y eléctricos.")

    with col_m2:
        st.markdown("**Distribución por tipo de vendedor**")
        vendor_counts = dff["seller_type"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            vendor_counts,
            labels=vendor_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=sns.color_palette(PALETTE, len(vendor_counts)),
            radius=0.75,
        )
        ax.set_title("")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.caption("Las ventas entre particulares (Individual) representan la mayor parte del mercado de usados.")

st.divider()

# ──────────────────────────────────────────────
# 6. TABLA DE DATOS
# ──────────────────────────────────────────────
st.subheader("TABLA DE DATOS")

cols_show = ["name", "year", "selling_price", "km_driven", "fuel",
             "seller_type", "transmission", "owner", "mileage",
             "engine", "max_power", "seats", "antiguedad", "precio_por_antiguedad"]

n_rows = st.slider("Filas a mostrar", 5, 100, 9, step=5)
st.dataframe(
    dff[cols_show].sort_values("selling_price", ascending=False).head(n_rows),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ──────────────────────────────────────────────
# 7. CONCLUSIONES
# ──────────────────────────────────────────────
st.subheader("CONCLUSIONES")

st.info(
    f"A partir del análisis exploratorio y las visualizaciones obtenidas, se identificaron los siguientes hallazgos:"
)
with st.container(border=True):
    st.markdown("#### 1. Depreciación y Valor")
    st.write(
        "La antigüedad es la variable con mayor influencia en el precio. "
        "Los vehículos más recientes concentran los valores de venta más altos."
    )

with st.container(border=True):
    st.markdown("#### 2. Impacto del Kilometraje")
    st.write(
        "Existe una relación negativa entre kilometraje y precio. "
        "A medida que aumenta el uso del vehículo, su valor de mercado disminuye."
    )

with st.container(border=True):
    st.markdown("#### 3. Configuración y Motor")
    st.write(
        "Los vehículos automáticos presentan precios promedio superiores a los manuales, "
        "lo que refleja una preferencia por configuraciones de mayor gama."
    )

with st.container(border=True):
    st.markdown("#### 4. Tipo de Combustible")
    st.write(
        "El mercado está dominado por vehículos Diesel y Gasolina, mientras que las alternativas "
        "como GNC o eléctricos tienen una participación reducida."
    )

with st.container(border=True):
    st.markdown("#### 5. Actores del Mercado")
    st.write(
        "La mayoría de las transacciones son realizadas por propietarios particulares, "
        "lo que evidencia un mercado principalmente orientado a la venta directa."
    )

with st.container(border=True):
    st.markdown("#### 6. Segmento de Lujo")
    st.write(
        "Marcas premium como Land Rover, Mercedes-Benz y Audi generan valores atípicos "
        "que elevan considerablemente la distribución de precios."
    )