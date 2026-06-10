import pandas as pd
import numpy as np

# =======================
# CARREGAR CSV
# =======================

df = pd.read_csv('drinks.csv')

# =======================
# RENOMEAR COLUNAS
# =======================

df.columns = [
    "Pais",
    "Cerveja",
    "Destilados",
    "Vinho",
    "LitrosAlcool"
]

# =======================
# VISUALIZAÇÃO INICIAL
# =======================

print("=== PRIMEIRAS 5 LINHAS ===")
print(df.head())

print("\n=== INFORMAÇÕES DO DATAFRAME ===")
print(df.info())

print("\n=== ESTATISTICAS GERAIS ===")
print(df.describe())

# ==========================
# ESTATÍSTICAS COM NUMPY
# ==========================

print("\n=== ESTATISTICAS DE CERVEJA ===")

print(f"Média: {np.mean(df['Cerveja']):.2f}")
print(f"Mediana: {np.median(df['Cerveja']):.2f}")
print(f"Maior Consumo: {np.max(df['Cerveja']):.2f}")
print(f"Menor Consumo: {np.min(df['Cerveja']):.2f}")
print(f"Desvio Padrão: {np.std(df['Cerveja']):.2f}")

# ==========================
# TOP 10 CERVEJA
# ==========================

print("\n=== TOP 10 PAISES QUE MAIS CONSOMEM CERVEJA ===")

top10 = df.nlargest(10, "Cerveja")
print(
    top10[
        ["Pais","Cerveja"]
    ]
)


# ==========================
# TOP 10 VINHO
# ==========================

print("\n=== TOP 10 PAISES QUE MAIS CONSOMEM VINHO ===")

top10 = df.nlargest(10, "Vinho")
print(
    top10[
        ["Pais","Vinho"]
    ]
)

# ==========================
# FILTROS
# ==========================

mediaAlcool = df['LitrosAlcool'].mean()
print("\n=== ACIMA DA MEDIA DE ALCOOL ===")
print(
    df[
        df["LitrosAlcool"] > mediaAlcool][["Pais","LitrosAlcool"]]
)

# ==========================
# NOVA COLUNA TOTAL
# ==========================

df["TotalBebidas"] = (
    df["Cerveja"] +
    df["Destilados"] + 
    df["Vinho"]    
)
print("\n=== TOTAL DE BEBIDAS ===")
print(df[["Pais","TotalBebidas"]].head())

# ==========================
# CLASSIFICAÇÃO COM O NUMPY
# ==========================

condicoes = [
    df["LitrosAlcool"] < 2,
    df["LitrosAlcool"] < 5,
    df["LitrosAlcool"] < 8,
    df["LitrosAlcool"] >= 8
]

categorias = [
    "Muito Baixo",
    "Baixo",
    "Médio",
    "Alto"
]

df["NivelConsumo"] = np.select(
    condicoes,
    categorias,
    default = "Não Informado"
)

print("\n=== CLASSIFICAÇÃO DE CONSUMO ===")

print(
    df[
        ["Pais", "LitrosAlcool", "NivelConsumo"]
    ].head(20)
)

# ==========================
# CONTAGEM POR CATEGORIA
# ==========================

print("\n=== QUANTIDADE DE PAISES POR NIVEL ===")
print(df["NivelConsumo"].value_counts())

# ==========================
# PAÍS COM MAIOR CONSUMO TOTAL
# ==========================

maiorConsumo = df.loc[df["TotalBebidas"].idxmax()]
print("\n=== MAIOR CONSUMIDOR ===")
print(maiorConsumo)

# ==========================
# ACIMA DA MÉDIA EM TUDO
# ==========================

mediaCerveja = df["Cerveja"].mean()
mediaDestilados = df["Destilados"].mean()
mediaVinho = df["Vinho"].mean()
print("\n=== ACIMA DA MEDIA EM TODAS AS BEBIDAS ===")
resultado = df[
    (df["Cerveja"] > mediaCerveja) &
    (df["Destilados"] > mediaDestilados) &
    (df["Vinho"] > mediaVinho)
]
print(
    resultado[["Pais","Cerveja","Destilados","Vinho"]]
)

# ==========================
# CORRELAÇÃO
# ==========================

print("\n=== MAIOR CORRELAÇÃO ===")

print(
    df[
        [
            "Cerveja",
            "Destilados",
            "Vinho",
            "LitrosAlcool"
        ]
    ].corr()
)

# ==========================
# ORDENAÇÃO
# ==========================

print("\n=== TOP 20 CONSUMO TOTAL ===")

print(
    df.sort_values(by="TotalBebidas", ascending=False)[["Pais", "TotalBebidas"]].head(20)
)

# ==========================
# SALVAR CSV
# ==========================

df.to_csv("drinks_processados.csv", index = False)