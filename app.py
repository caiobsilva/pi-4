from flask import Flask, render_template, request, redirect, url_for
from pi4 import gerar_mapa_gastos

app = Flask(__name__)

def before_request():
        app.jinja_env.cache = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('head-map.html')

@app.route('/foo', methods=['GET', 'POST'])
def foo(anos=[]):
        ano = 0
        if request.method == "GET":
                return render_template("head-map.html", anos=anos)

        #recebe o value do botão de submit. 
        ano = int(request.form.get('text_input', None))

        #gera o mapa coroplético de gastos.
        gerar_mapa_gastos(ano)

        #log de anos
        anos.append(ano)

        print("Atualizando mapa para: " + str(ano))
        return redirect(url_for('foo'))

if __name__ == '__main__':
    #app.before_request(before_request)
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    #app.jinja_env.auto_reload = True
    #TEMPLATES_AUTO_RELOAD=True
    app.run(debug=True)