import numpy as np 

arr = np.array([1, 2, 3, 4, 5])

print("Array Numpy:")
print(arr)

# Operações matematicas com array
print('\nArray multiplicado por 2:')
print(arr * 2)

#Operações entre arrays
arr2 = np.array([6, 7, 8, 9, 10])
print('\nSomando duas Arrays:')
print(arr + arr2)

 # Criando uma matriz
matriz = np.array(
    [
        [1, 2, 3],
        [4, 5, 6]
    ]
)
print('\nMatriz 2x3:')
print(matriz)

#Soma de uma matriz
print('\nSoma:')
print(np.sum(matriz))

# Media da matriz
print('\nMedia:')
print(np.mean(matriz))

# Transposta da matriz
print('\nMatriz Transposta:')
print(matriz.T)

# Gerando numeros aleatorios
print('\nNumeros aleatorios entre 0 e 1:')
print(np.random.rand(3,3))