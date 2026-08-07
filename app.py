import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Anúncios de venda de carros",
    page_icon="🚗",
    layout="wide",
)


@st.cache_data
def carregar_dados(caminho="vehicles_us.csv"):
    """Lê o CSV e faz uma limpeza mínima para o painel."""
    car_data = pd.read_csv(caminho)

    # ausente em is_4wd significa "não é 4x4"
    car_data["is_4wd"] = car_data["is_4wd"].fillna(0).astype(int)
    car_data["paint_color"] = car_data["paint_color"].fillna("desconhecida")
    car_data["date_posted"] = pd.to_datetime(car_data["date_posted"])

    # a primeira palavra da coluna model é a fabricante
    car_data["manufacturer"] = car_data["model"].str.split().str[0]

    # idade do veículo na data do anúncio
    car_data["age"] = car_data["date_posted"].dt.year - car_data["model_year"]

    return car_data


car_data = carregar_dados()

st.header("🚗 Painel de anúncios de venda de carros")
st.write(
    """
    Este painel explora um conjunto de anúncios de venda de carros nos Estados Unidos.
    Use os filtros da barra lateral para recortar os dados e as caixas de seleção abaixo
    para construir os gráficos.
    """
)

# ---------------------------------------------------------------------------
# Filtros
# ---------------------------------------------------------------------------
st.sidebar.header("Filtros")

tipos = sorted(car_data["type"].unique())
tipos_selecionados = st.sidebar.multiselect(
    "Tipo de veículo",
    options=tipos,
    default=tipos,
)

condicoes = sorted(car_data["condition"].unique())
condicoes_selecionadas = st.sidebar.multiselect(
    "Condição",
    options=condicoes,
    default=condicoes,
)

preco_min, preco_max = st.sidebar.slider(
    "Faixa de preço (US$)",
    min_value=int(car_data["price"].min()),
    max_value=int(car_data["price"].max()),
    value=(1000, 50000),
    step=500,
)

excluir_outliers = st.sidebar.checkbox(
    "Excluir outliers de odômetro (acima de 400.000 milhas)",
    value=True,
)

dados_filtrados = car_data[
    car_data["type"].isin(tipos_selecionados)
    & car_data["condition"].isin(condicoes_selecionadas)
    & car_data["price"].between(preco_min, preco_max)
]

if excluir_outliers:
    dados_filtrados = dados_filtrados[
        dados_filtrados["odometer"].isna() | (dados_filtrados["odometer"] <= 400_000)
    ]

if dados_filtrados.empty:
    st.warning("Nenhum anúncio corresponde aos filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ---------------------------------------------------------------------------
# Métricas gerais
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Anúncios", f"{len(dados_filtrados):,}".replace(",", "."))
col2.metric("Preço mediano", f"US$ {dados_filtrados['price'].median():,.0f}".replace(",", "."))
col3.metric("Odômetro mediano", f"{dados_filtrados['odometer'].median():,.0f} mi".replace(",", "."))
col4.metric("Dias no site (média)", f"{dados_filtrados['days_listed'].mean():.0f}")

with st.expander("Ver amostra dos dados filtrados"):
    st.dataframe(dados_filtrados.head(50), use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Botões: histograma e gráfico de dispersão
# ---------------------------------------------------------------------------
st.subheader("Gráficos sob demanda")

col_botao1, col_botao2 = st.columns(2)
hist_button = col_botao1.button("Criar histograma", use_container_width=True)
scatter_button = col_botao2.button("Criar gráfico de dispersão", use_container_width=True)

if hist_button:
    st.write("Criando um histograma da quilometragem (odômetro) dos anúncios")

    fig = px.histogram(
        dados_filtrados,
        x="odometer",
        nbins=50,
        title="Distribuição do odômetro",
        labels={"odometer": "Odômetro (milhas)"},
    )
    fig.update_layout(yaxis_title="Número de anúncios")

    st.plotly_chart(fig, use_container_width=True)

if scatter_button:
    st.write("Criando um gráfico de dispersão de odômetro versus preço")

    fig = px.scatter(
        dados_filtrados,
        x="odometer",
        y="price",
        color="condition",
        opacity=0.5,
        title="Odômetro versus preço",
        labels={
            "odometer": "Odômetro (milhas)",
            "price": "Preço (US$)",
            "condition": "Condição",
        },
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Caixas de seleção: análises adicionais
# ---------------------------------------------------------------------------
st.subheader("Análises adicionais")

build_histogram = st.checkbox("Comparar a distribuição de preços por condição do veículo")

if build_histogram:
    st.write("Criando um histograma de preços separado por condição do veículo")

    fig = px.histogram(
        dados_filtrados,
        x="price",
        color="condition",
        nbins=60,
        barmode="overlay",
        opacity=0.7,
        title="Distribuição de preços por condição",
        labels={"price": "Preço (US$)", "condition": "Condição"},
    )
    fig.update_layout(yaxis_title="Número de anúncios")

    st.plotly_chart(fig, use_container_width=True)

build_scatter = st.checkbox("Relacionar a idade do veículo com o preço")

if build_scatter:
    st.write("Criando um gráfico de dispersão de idade do veículo versus preço")

    dados_idade = dados_filtrados.dropna(subset=["age"])

    fig = px.scatter(
        dados_idade,
        x="age",
        y="price",
        color="type",
        opacity=0.5,
        title="Idade do veículo versus preço",
        labels={
            "age": "Idade do veículo (anos)",
            "price": "Preço (US$)",
            "type": "Tipo",
        },
    )

    st.plotly_chart(fig, use_container_width=True)

build_box = st.checkbox("Comparar preços entre os tipos de veículo")

if build_box:
    st.write("Criando um boxplot de preços por tipo de veículo")

    fig = px.box(
        dados_filtrados,
        x="type",
        y="price",
        color="type",
        title="Preço por tipo de veículo",
        labels={"type": "Tipo", "price": "Preço (US$)"},
    )
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

build_top_manufacturers = st.checkbox("Ver as fabricantes com mais anúncios")

if build_top_manufacturers:
    st.write("Criando um gráfico de barras com as 15 fabricantes mais anunciadas")

    top = (
        dados_filtrados["manufacturer"]
        .value_counts()
        .head(15)
        .rename_axis("manufacturer")
        .reset_index(name="anuncios")
    )

    fig = px.bar(
        top,
        x="manufacturer",
        y="anuncios",
        title="Fabricantes com mais anúncios",
        labels={"manufacturer": "Fabricante", "anuncios": "Número de anúncios"},
    )

    st.plotly_chart(fig, use_container_width=True)
