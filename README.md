# 📊 Dashboard NBA

Este é um dashboard interativo desenvolvido com **Streamlit** para visualizar e comparar estatísticas de jogadores da **NBA** em tempo real. Ele utiliza a biblioteca [nba-api](https://github.com/swar/nba_api) para obter os dados oficiais da liga.

## 🔥 Funcionalidades

- Comparação lado a lado entre dois jogadores
- Visualização de estatísticas como Pontos, Assistências, Rebotes, Roubos, Tocos e Pontuação Fantasy
- Ranking dos Top 25 jogadores por estatística selecionada
- Ranking dos Top 25 jogadores por Fantasy Points
- Visualizações com **Plotly** (barras interativas)

## 📸 Exemplos de Tela

> *(Você pode adicionar capturas de tela aqui usando `![screenshot](caminho/para/imagem.png)` ou subir as imagens no repositório)*

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/mucarii/Dashboard-NBA.git
cd Dashboard-NBA
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode o app com Streamlit

```bash
streamlit run app.py
```

## 🧠 Como funciona

Os dados são obtidos usando a `nba_api`, processados e exibidos em visualizações usando `Plotly`. A lógica de cálculo dos pontos Fantasy é baseada nos critérios personalizados que você pode ajustar em `src/fantasy_calc.py`.

## 🧰 Tecnologias Usadas

- Python
- Streamlit
- Plotly
- Pandas
- nba-api

## 📁 Estrutura de Pastas

```
Dashboard-NBA/
├── app.py
├── requirements.txt
├── src/
│   ├── nba_stats.py
│   └── fantasy_calc.py
└── README.md
```

## 🙋‍♂️ Autor

Feito por **[Murilo Calore](https://github.com/mucarii)**  
Se quiser me chamar pra bater um papo ou colaborar, só mandar mensagem!