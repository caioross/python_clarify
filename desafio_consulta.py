import json, requests

nome01 = input("Escolha seu primeiro nome: \n R: ")
nome02 = input("Escolha seu segundo nome: \n R: ")

resultado01 = requests.get(f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome01}")

resultado02 = requests.get(f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome02}")

resultado01 = json.loads(resultado01.text)
resultado02 = json.loads(resultado02.text)

print(f"-----------------------\n Nome: {nome01} \n")
print(resultado01[0]['res'])

print(f"-----------------------\n Nome: {nome02} \n")
print(resultado02[0]['res'])