#Importando bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import sqlite3

# Seleciona Arquivo CSV
path = './data/dataset_desafio_fadesp.csv'
df = pd.read_csv(path,encoding='ISO-8859-1')

# Executa limpeza dos Dados excluíndo valores nulos ou duplicados
df.isnull().sum()
df = df.dropna()
df.isnull().sum()
df = df.drop_duplicates()
df.duplicated().sum()

# Salva os dados do Dataframe no Banco de Dados SQLite
conn = sqlite3.connect('product.db')
df.to_sql('product', conn, if_exists='replace', index=False)
conn.close()

# Recupera os dados do Banco 
conn = sqlite3.connect('product.db')
query = "SELECT * FROM product"
df = pd.read_sql(query, conn)
conn.close()

# Relação De Dias e Vendas
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x="Order Date", bins=30)
plt.title("Distribuição das vendas por dia")
plt.xlabel("Data da venda")
plt.ylabel("Quantidade de vendas")
plt.show()

# Agrupando os dados por estado e produto e calculando a quantidade de vendas e a receita total
estado_produto_df = df.groupby(["State", "Product Name"]).agg({"Quantity": sum, "Sales": sum}).reset_index()
estado_produto_df

# Extraindo os 5 estados com mais vendas
top_5_estados = estado_produto_df.groupby("State").agg({"Sales": sum}).reset_index()
top_5_estados = top_5_estados.sort_values("Sales", ascending=False).head(5)
top_5_estados

# Gráfico de barras empilhadas da quantidade de vendas por produto e estado
graf = top_5_estados.plot(kind='bar', stacked=True)
graf.set_title("Distribuição geográfica dos produtos mais vendidos")
graf.set_xlabel("Quantidade de vendas")
graf.set_ylabel("Produto")
plt.show()

# Transformar as colunas Order e Ship para data
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Order Date'] = pd.to_datetime(df['Order Date'])

#Criar coluna com diferença entre datas de entrega
df['dif_datas'] = df['Order Date'] - df['Ship Date']
df['dif_datas']

# Gráfico de dispersão da quantidade de vendas e data de saída
plt.figure(figsize=(12, 6))
plt.scatter(data=df, x="Ship Date", y="Sales")
plt.title("Relação entre a quantidade de vendas e a data de saída")
plt.xlabel("Data de saída")
plt.ylabel("Quantidade de vendas")
plt.show()