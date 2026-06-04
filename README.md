# Pulso Urbano — Criminalidade em Grandes Cidades Brasileiras

Projeto de análise e visualização de dados sobre criminalidade no Brasil entre 2015 e 2024.

## Sobre

Dashboard interativo desenvolvido em Streamlit que permite explorar padrões de criminalidade em grandes cidades brasileiras, com KPIs, filtros interativos, gráficos temporais e análises regionais.

## Estrutura do Projeto

```
projeto-criminalidade/
├── app.py                  # Dashboard Streamlit
├── requirements.txt        # Dependências
├── index.html              # Página GitHub Pages
├── README.md
├── dados/
│   └── simulacao_criminalidade_brasil.csv
├── notebooks/
│   └── analise_criminalidade.ipynb
├── database/               # SQLite gerado ao rodar o notebook
├── imagens/
│   └── logo.png
└── src/
    ├── components.py
    ├── data.py
    ├── style.py
    └── pages/
        ├── visao_geral.py
        ├── temporal.py
        ├── cidades.py
        ├── crimes.py
        ├── mapa.py
        └── dados.py
```

## Tecnologias

- Python 3.11+
- Pandas
- Matplotlib / Seaborn
- Plotly
- Streamlit
- SQLAlchemy + SQLite
- GitHub Pages

## Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar o dashboard
streamlit run app.py
```

## Links

- **GitHub Pages:** https://namxsj.github.io/pulso-urbano/
- **Dashboard Streamlit:** https://pulso-urbano.streamlit.app/

## Funcionalidades

- KPIs: total de ocorrências, vítimas, prisões, índice de violência
- Filtros por ano, região, estado, cidade, tipo de crime e nível de risco
- Evolução temporal da criminalidade
- Comparativo entre cidades e regiões
- Análise por tipo de crime e período do dia
- Mapa interativo com distribuição geográfica
- Tabela de dados com exportação CSV

## Autor

Projeto G2 — Tema 15 | Análise e Visualização de Dados — La Salle | Júlia Bittencourt & Mariana Moura
