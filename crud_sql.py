import sqlite3

# Criar o banco de dados  ( ou criar se caso não existir)
def conectarBanco() :
    conexao = sqlite3.connect('meu_banco.db')
    return conexao

# criaremos uma tabela nesse banco de dados
def criarTabela() :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER
        )
    ''')
    conexao.commit()
    conexao.close()

def inserirUsuarios(nome, idade) :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, idade)
        VALUES (?, ?)               
    ''', (nome, idade))
    conexao.commit()
    conexao.close()
    
def listarUsuarios() :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        print(usuario)
    conexao.close()
    
def AtualizarUsuario(id, novoNome, novaIdade) :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE usuarios 
        SET nome = ?, idade = ?
        WHERE id = ?               
    ''',(novoNome, novaIdade, id))
    conexao.commit()
    conexao.close()

def excluirUsuario(id) :
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute('''
        DELETE FROM usuarios
        WHERE id = ?               
    ''', (id,))
    conexao.commit()
    conexao.close()

criarTabela()

inserirUsuarios("Caio", 39)
inserirUsuarios("Leandro", 39)
inserirUsuarios("Carlos", 58)
inserirUsuarios("Guilherme", 25)
inserirUsuarios("Daniel", 30)
inserirUsuarios("Vinicius", 22)
listarUsuarios()
print('----------Depois de editar------------')
AtualizarUsuario(3, 'Thamires', 35)
listarUsuarios()

nomes = ['Adelaide','Abelardo','Juvencio','Roberval','Silverio','Celestino','Zacarias','Ambrosio']

for nome in nomes :
    inserirUsuarios(nome, 1)
    
excluirUsuario(12)
listarUsuarios()