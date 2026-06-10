def divisao(a, b):
    try:
            # Tentando dividir dois numeros normalmente.
        resultado = a / b
        print(f"O resultado da divisão de {a} por {b} é {resultado}")
    except ZeroDivisionError:
        # Se houver um erro de divisão por zero o codigo dentro do except é executado
        print("Erro: Não é possivel dividir por zero.")
    except TypeError:
        # Caso os parametros fornecidos nao sejam numerocs o codigo dentro desse except é executado
        print("Erro: Ambos os valores devem ser numeros.")
    except Exception as e:
        # Captura qualquer outro tipo de exceção que nao tenha sido tratada nos excepts anteriores
        print(f"Erro inesperado {e}")
    else:
        # O bloco else é executado se o codigo dentro do try for bem sucedido (sem erros)
        print("Divisão realizada com sucesso!")
    finally:
        # O bloco finally sempre será executado, independente de erro ou sucesso
        print("Processo de divisão concluido.")
    
# Teste 01: Divisão normal
print("\n--- Teste 01 ---\n")
divisao(10,2)

# Teste 02: Divisão por zero
print("\n--- Teste 02 ---\n")
divisao(10,0)

# Teste 03: Divisão com tipos invalidos
print("\n--- Teste 03 ---\n")
divisao(10, "dois")

# Teste 04: Divisão com erro inesperado
print("\n--- Teste 04 ---\n")
divisao("dez", 2)