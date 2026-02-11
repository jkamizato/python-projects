import pandas as pd
import matplotlib.pyplot as plt

print("📂Loading data...")

csv_url = 'https://www.camara.leg.br/cotas/Ano-2025.csv.zip'
df = pd.read_csv(csv_url, compression='zip', sep=';', encoding='utf-8', low_memory=False)

# Renomear colunas para facilitar
df.rename(columns={
    'txNomeParlamentar': 'Deputado',
    'sgPartido': 'Partido',
    'sgUF': 'UF',
    'vlrLiquido': 'Valor',
    'txtDescricao': 'Categoria'
}, inplace=True)

print(f"✅ Dados carregados: {df.shape[0]} registros encontrados.")

# P1: Qual o total gasto no ano?
total_gasto = df['Valor'].sum()
print(f"💰 Total Gasto na Cota: R$ {total_gasto:,.2f}")

# P2: Ranking dos 5 Deputados que mais gastaram
top_spenders = df.groupby(['Deputado', 'Partido', 'UF'])['Valor'].sum().sort_values(ascending=False).head(10)
print("\n🏆 Top 10 Deputados 'Gastões':")
print(top_spenders)


# Gasto dos Deputados por Estado
total_gasto_por_estado = df.groupby(['UF'])['Valor'].sum().sort_values(ascending=False).head(10)
print("\n 🚩 Top 10 Estados que mais gastam: ")
print(total_gasto_por_estado)

# Agrupamento por estado
analise_uf = df.groupby('UF').agg({
    'Valor': 'sum',
    'Deputado': 'nunique',
}).reset_index()

# 2. Agora criamos a coluna calculada (Aritmética de Colunas)
# Essa é a mágica da vetorização: dividimos a coluna inteira de uma vez
analise_uf['Media_Por_Parlamentar'] = analise_uf['Valor'] / analise_uf['Deputado']

# 3. Ordenamos pelo "Deputado mais caro"
ranking_real = analise_uf.sort_values(by='Media_Por_Parlamentar', ascending=False)

# 4. Melhorando a visualização
# Vamos renomear para ficar claro no print
ranking_real.rename(columns={
    'Valor': 'Gasto_Total_Estado',
    'Deputado': 'Qtd_Deputados'
}, inplace=True)

# Formatando para ler fácil
display_ranking = ranking_real.copy()
display_ranking['Gasto_Total_Estado'] = display_ranking['Gasto_Total_Estado'].map('R$ {:,.2f}'.format)
display_ranking['Media_Por_Parlamentar'] = display_ranking['Media_Por_Parlamentar'].map('R$ {:,.2f}'.format)

print("--- Ranking Real: Custo Médio por Deputado em cada Estado ---")
print(display_ranking)


# P3: Com o que eles mais gastam? (Categorias)
# gastos_categoria = df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)

# 4. Visualização (O "Ouro" do GitHub)
# Vamos gerar um gráfico de barras das 5 maiores categorias de gasto
# plt.figure(figsize=(10,6))
# gastos_categoria.head(5).plot(kind='barh', color='salmon')
# plt.title('Top 5 Categorias de Gastos da Câmara (2023)')
# plt.xlabel('Valor Total (R$)')
# plt.ylabel('Categoria')
# plt.tight_layout()
#
# # Salvar o gráfico para colocar no README do GitHub
# plt.savefig('grafico_gastos.png')
# print("\n📊 Gráfico gerado com sucesso: grafico_gastos.png")