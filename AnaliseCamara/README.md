# 🏛️ Auditando Brasília: Análise da Cota Parlamentar

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Analise-150458?style=flat&logo=pandas&logoColor=white)

## Sobre o projeto

Com o intuito de analisar dados reais, que poderiam de alguma forma me ajudar a estudar Pandas e também análise de dados, resolvi utilizar os dados abertos dos gastos dos parlamentares.

Criei este script em Python para "mastigar" esses dados brutos da Câmara dos Deputados.

O maior desafio técnico aqui foi lidar com a sujeira dos dados (tipagem errada, formatação brasileira de moeda) e criar métricas que fossem justas, fugindo do óbvio "Total Gasto".

## 💡 O que o código faz

1.  **Baixa e Carrega:** Pega o CSV direto da fonte oficial (ou local).
2.  **Limpa a bagunça:** Trata colunas que misturam texto e números e converte moedas formatadas (R$) para float.
3.  **Analisa:**
    *   Agrupa gastos por Estado e Partido.
    *   **O Pulo do Gato:** Calcula o *Gasto Médio por Parlamentar*. (Olhar apenas o total absoluto é injusto, já que SP tem 70 deputados e o Acre tem 8. O script normaliza isso).

---

## 📊 Resultados Interessantes

Rodando a análise de 2025, percebi que:

*   **O Ranking muda:** Quando olhamos o gasto *per capita* (por cabeça), estados do Norte e Nordeste costumam liderar. Isso faz sentido logisticamente: passagens aéreas de Roraima para Brasília são muito mais caras do que de Goiás para Brasília. Ainda preciso comparar com os impostos arrecadados por Estados, para entender o quão caro é um deputado por estado.
*   **Categorias:** A maior parte da verba não vai para cafezinho, mas sim para "Divulgação da Atividade Parlamentar" e passagens.

---

## 🛠️ Stack

*   **Python 3**
*   **Pandas:** Para toda a mágica de ETL e agregação.
*   **Matplotlib:** Para gerar os gráficos.

---

## 💻 Como rodar na sua máquina

Se quiser testar ou modificar a análise:

1.  Clone o repo e na pasta correspondente, rodar:
```bash
python main.py