import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

print("Baixando dados...")
tickers = ['BTC-USD', 'AAPL', 'BRL=X', 'MMM']

# Baixa os dados
dados = yf.download(tickers, period="1y")['Close']

# --- A CORREÇÃO MÁGICA ---
# 1. ffill(): Preenche buracos (feriados/fds) com o valor do dia anterior
# 2. bfill(): Se o PRIMEIRO dia for feriado, preenche com o valor do dia seguinte
# 3. dropna(): Se sobrar algum lixo, remove a linha
dados = dados.ffill().bfill().dropna()

print("Dados limpos! Primeiras linhas:")
print(dados.head()) # Mostra no terminal para conferir

# Normaliza (Base 100)
dados_normalizados = (dados / dados.iloc[0]) * 100

print(type(dados))

print("Gerando gráfico...")
fig = go.Figure()

for coluna in dados_normalizados.columns:
    fig.add_trace(go.Scatter(
        x=dados_normalizados.index,
        y=dados_normalizados[coluna],
        mode='lines',
        name=coluna
    ))

fig.update_layout(
    title="Comparativo de Investimentos (Base 100)",
    xaxis_title="Data",
    yaxis_title="Variação (%)",
    template="plotly_dark",
    hovermode="x unified" # Dica Pro: Mostra todos os valores juntos ao passar o mouse
)

fig.show()