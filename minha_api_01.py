from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1> Oláaaaa Mundo! </h1> <br> <h2>Sou um subtitulo</h2>"

@app.route('/sobre')
def sobre():
    return '''
       <!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Sobre</title><style>*{margin:0;padding:0;box-sizing:border-box}body{display:flex;justify-content:center;align-items:center;height:100vh;background:linear-gradient(-45deg,#0f172a,#1e293b,#334155,#0f172a);background-size:400% 400%;animation:bg 12s ease infinite;font-family:Arial,sans-serif;color:#fff;overflow:hidden}.card{padding:40px 50px;border-radius:20px;background:rgba(255,255,255,.08);backdrop-filter:blur(12px);text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.3);animation:fadeIn 1.2s ease}.card h1{font-size:2.5rem;margin-bottom:15px;background:linear-gradient(90deg,#38bdf8,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.card p{font-size:1.1rem;opacity:.9}.glow{position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(56,189,248,.15);filter:blur(80px);animation:float 8s ease-in-out infinite}@keyframes bg{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}@keyframes fadeIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}@keyframes float{0%,100%{transform:translate(-100px,-50px)}50%{transform:translate(100px,50px)}}</style></head><body><div class="glow"></div><div class="card"><h1>Sobre</h1><p>Esta página foi desenvolvida por <strong>Caio Comitre Rossi</strong>.</p></div></body></html> 
    '''
    
@app.route('/ola/<nome>')
def ola(nome):
    return f"<h1>Olá {nome}</h1>"

if __name__ == '__main__':
    app.run(debug=True)