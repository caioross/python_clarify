import pandas as pd

# Dados dos funcionarios
dados = {
    "Nome":['Maria','João','Marcos','Ana','Mariana'],
    "Idade":[28, 42, 31, 24, 36],
    "Cargo":['Analista','Gerente','Desenvolvedor','Estagiaria','Analista'],
    "Salario":[5500, 9000, 7500, 2500, 6200]
}

# Criando o DataFrame
df = pd.DataFrame(dados)
#Exibindo o DataFrame completo:
print("=== DataFrame Completo ===")
print(df)

# Exibir apenas a coluna Cargo
print('\n=== Apenas Cargos: ===')
print(df['Cargo'])

# Exibir apenas funcionarios com salario maior que 6000
print("\n=== Salário maior que R$ 6000 ===")
print(df[df['Salario'] > 6000])

# Funcionarios com idade menor que 35
print("\n=== Idade menor que 35 anos ===")
print(df[df['Idade'] < 35])

# Criar uma coluna de bonus de 15%
df['Bonus'] = df=['Salario'] * 0.15

# Criar uma coluna de salario final (Salario+Bonus)
df['Salario Final'] =  df['Salario'] + df['Bonus']
print("\n=== DataFrame com Bônus e Salário Final ===")
print(df)

# Estatisticas
print('\n=== Estatisticas ===')
print(f"Media Salarial: R$ {df['Salario'].mean():.2f}")
print(f"Maior Salario: R$ {df['Salario'].max():.2f}")
print(f"Menor Salario: R$ {df['Salario'].min():.2f}")

# Ordenado por salario
print('\n=== Funcionarios ordenados por salario ===')
print(df.sort_values(by='Salario', ascending=False))

# Quantidade por cargo
print('\n=== Quantidade por cargo ===')
print(df["Cargo"].value_counts())

# Funcionarios cujo nome começa com M
print("\n=== Funcionarios com nome iniciando em 'M' ===")
print(df[df['Nome'].str.startswith("M")])

# Funcionarios com maior salario final
maiorSalarioFinal = df.loc[df['Salario Final'].idxmax()]
print('\n=== Funcionario com Maior Salario Final ===')
print(maiorSalarioFinal)

# Salvando em CSV
df.to_csv("funcionarios.csv", index=False)
print('\nArquivo "funcionario.csv" salvo com sucesso.')
