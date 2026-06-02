from random import randint

print("########     Iniciando o Jogo!     #######")


random = randint(0, 100)
chute = 0
chances = 10

# < Menor
# > Maior
# == Igual (Comparação)
# != Diferente (Comparação)
# >= Maior ou igual (A Partir de tal valor)
# <= Menor ou Igual (Até tal valor)

while chute != random :
    chute = input("Chute um numero entre 0 e 100")
    if chute.isnumeric() :
        chute = int(chute)
        chances = chances - 1
        if chute == random :
            print('')
            print('Parabéns, você venceu! O numero era {} e você ainda tinha {} chances.'.format(random, chances))
            print('')
            break
        else :
            print('')
            if chute > random  :
                print('Você errou! Dica: É um numero menor.')
            else:
                print('Você errou! Dica: É um numero maior.')
            print('Você possui ainda {} chances.'.format(chances))
            print('')
        if chances == 0 :
            print('')
            print('Suas chances acabaram, você perdeu! O Numero era: {}'.format(random))
            print('')
            break
       
        
print("########     Fim de Jogo!     #######")
