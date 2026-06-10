class Carro :
    def __init__ (self, modelo, cor) :
    # Atributos do que é um Carro
        self.modelo = modelo
        self.cor = cor
        self.velocidade = 0
    
    def acelerar(self, incremento) :
    #Ação que um objeto carro pode fazer
        self.velocidade += incremento
        print(f"O carro {self.modelo} acelerou para {self.velocidade}km/h")
    
    def parar(self) :
        self.velocidade = 0
        print(f"O carro {self.modelo} parou")
    
carro_instrutor = Carro("Jimny", "Verde")
carro_carlos = Carro("Corola", "Chumbo")
carro_leandro = Carro("Etios", "Cinza")
carro_guilherme = Carro("Fit", "Prata")

carro_instrutor.acelerar(10)
carro_instrutor.acelerar(10)
carro_instrutor.acelerar(10)
carro_instrutor.acelerar(10)
carro_instrutor.parar()