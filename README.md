# 🚗 Painel de anúncios de venda de carros

Aplicativo web interativo que explora um conjunto de **51.525 anúncios de venda de carros
usados nos Estados Unidos**. O painel permite filtrar os anúncios e gerar visualizações
sob demanda para responder perguntas como: quanto a quilometragem derruba o preço? Que
tipo de carroceria é mais cara? Como a condição declarada se reflete no valor pedido?

O projeto foi construído com **pandas**, **Plotly Express** e **Streamlit**, e está
implantado no Render.

## 🌐 Aplicativo online

**URL:** https://SEU-APP.onrender.com/

> Substitua o endereço acima pela URL gerada pelo Render depois da implantação.
> Como o plano é gratuito, o aplicativo "adormece" após alguns minutos de inatividade —
> na primeira visita pode levar cerca de um minuto para carregar.

## ✨ Funcionalidades

**Filtros (barra lateral)**

- seleção de tipos de veículo (SUV, sedan, truck, pickup, ...);
- seleção da condição declarada (`new`, `like new`, `excellent`, `good`, `fair`, `salvage`);
- faixa de preço ajustável;
- opção de excluir outliers de odômetro (acima de 400.000 milhas).

**Indicadores** — número de anúncios, preço mediano, odômetro mediano e média de dias no
site, todos recalculados conforme os filtros.

**Gráficos sob demanda (botões)**

- **Criar histograma** — distribuição do odômetro;
- **Criar gráfico de dispersão** — odômetro versus preço, colorido por condição.

**Análises adicionais (caixas de seleção)**

- distribuição de preços separada por condição do veículo;
- idade do veículo versus preço, colorida por tipo de carroceria;
- boxplot de preços por tipo de veículo;
- as 15 fabricantes com mais anúncios.

## 📊 Conjunto de dados

`vehicles_us.csv` — anúncios de venda de carros com preço, ano do modelo, modelo, condição,
número de cilindros, combustível, odômetro, transmissão, tipo de carroceria, cor, tração
4x4, data de publicação e dias no site.

A análise exploratória completa (valores ausentes, tratamento dos dados, distribuições e
correlações) está em [notebooks/EDA.ipynb](notebooks/EDA.ipynb).

Principais achados:

- preço e odômetro têm distribuições bem assimétricas à direita, com valores extremos
  (preços de US$ 1 e odômetros de 990.000 milhas) que precisam ser recortados nos gráficos;
- quilometragem e idade se relacionam negativamente com o preço (correlações de -0,39 e
  -0,41), e a maior parte da desvalorização acontece nos primeiros dez anos;
- picapes e caminhões têm as medianas de preço mais altas; sedãs e hatchbacks, as mais baixas;
- o tempo que o anúncio fica no site não tem relação com o preço pedido.

## 🗂️ Estrutura do projeto

```
.
├── README.md
├── app.py                  # aplicativo Streamlit
├── requirements.txt        # dependências
├── vehicles_us.csv         # conjunto de dados
├── .streamlit
│   └── config.toml         # configuração de servidor para o Render
└── notebooks
    └── EDA.ipynb           # análise exploratória de dados
```

## 💻 Como executar localmente

```bash
# 1. clone o repositório
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO

# 2. crie e ative um ambiente virtual
python -m venv vehicles_env
source vehicles_env/bin/activate      # Linux / macOS
vehicles_env\Scripts\activate         # Windows

# 3. instale as dependências
pip install -r requirements.txt

# 4. execute o aplicativo
streamlit run app.py
```

O aplicativo abre em `http://localhost:10000` (porta definida em `.streamlit/config.toml`).

## ☁️ Implantação no Render

O serviço web foi configurado com:

- **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command:** `streamlit run app.py`

## 🛠️ Tecnologias

`Python` · `pandas` · `Plotly Express` · `Streamlit` · `Jupyter` · `Render`
