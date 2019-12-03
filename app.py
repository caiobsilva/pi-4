from flask import Flask, render_template, request, redirect, url_for
from pi4 import gerar_mapa_gasto
from pi4 import gerar_mapa_fundos

app = Flask(__name__)

def before_request():
        app.jinja_env.cache = {}

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/map-gastos')
def mapGastos():
        gerar_mapa_gasto(1994)
        return render_template('head-map-gasto.html')

@app.route('/map-fundos')
def mapFundos():
        gerar_mapa_fundos(2008)
        return render_template('head-map-fundo.html')

@app.route('/gastos', methods=['GET', 'POST'])
def gastos(anos=[]):
        ano = 0
        if request.method == "GET":
                return render_template("head-map-gasto.html", anos=anos)

        #recebe o value do botão de submit. 
        ano = int(request.form.get('text_input', None))

        #gera o mapa coroplético de gastos.
        gerar_mapa_gasto(ano)

        #log de anos
        anos.append(ano)

        print("Atualizando mapa para: " + str(ano))
        return redirect(url_for('gastos'))

@app.route('/fundos', methods=['GET', 'POST'])
def fundos(anos=[]):
        ano = 0
        if request.method == "GET":
                return render_template("head-map-fundo.html", anos=anos)

        #recebe o value do botão de submit. 
        ano = int(request.form.get('text_input', None))

        #gera o mapa coroplético de fundos.
        gerar_mapa_fundos(ano)

        #log de anos
        anos.append(ano)

        print("Atualizando mapa para: " + str(ano))
        return redirect(url_for('fundos'))

if __name__ == '__main__':
    #app.before_request(before_request)
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    #app.jinja_env.auto_reload = True
    #TEMPLATES_AUTO_RELOAD=True
    app.run(debug=True)