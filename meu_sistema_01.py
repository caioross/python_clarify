from flask import Flask, redirect, url_for, request, render_template
from requests import get

app = Flask(__name__)

@app.route('/')
def paginaInicial():
    return render_template('inicio.html')

@app.route('/acesso/')
def fazerLogin():
    return render_template('login.html')

@app.route('/welcome/')
def welcome() :
    return render_template('welcome.html')

@app.route("/validador/", methods=["POST", 'GET'])
def validador():
    meuUsuario = "caio"
    minhaSenha =  "123"
    # caso receba um post
    if request.method == 'POST':
        usuario = request.form['c_usuario']
        senha = request.form['c_senha']
        if usuario == meuUsuario and senha == minhaSenha:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('pagina403'))
    # Caso seja um GET
    else:
        usuario = request.args.get('c_usuario')
        senha = request.args.get('c_senha')
        if usuario == meuUsuario and senha == minhaSenha:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('pagina403'))
        
    
@app.route('/pagina403')
def pagina403() :
    return render_template('pagina403.html')

if __name__ == '__main__' :
    app.run(debug=True)