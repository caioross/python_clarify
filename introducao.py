print("Oi São Paulo")
# Isso é um comentario

palavra = "Caio"
contador = 0

for letra in palavra:
    print(str(contador) + " - " + letra)
    contador = contador + 1 
    
    
numero01 = "2"
numero02 = "2"
    
resultado = numero01 + numero02
print(resultado)


cidades = ["São Paulo","Rio de Janeiro","Poá","Recife"]
print(cidades[2])

for cidade in cidades :
    print(cidade)
    
botaoExecutar = True # ou True ou False : boolean
contador = 0

while botaoExecutar :
    print(contador)
    contador = contador + 1
    if contador >= 20 :
        botaoExecutar = False