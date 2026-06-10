class Calculadora :
    def somar(self, *args):
        return sum(args)
    
    def media(self, *args):
        return sum(args) / len(args)
    
calc = Calculadora()

print(calc.somar(1, 2))
print(calc.somar(1, 2, 3, 4, 5))