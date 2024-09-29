from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

df_estoque = pd.read_csv('estoque_geladeira.csv')
temperatura = 16
porta_Aberta = False

@app.route('/')
def index():
    return render_template('index.html', estoque=df_estoque.to_dict(orient='records'))

@app.route('/abastecer', methods=['POST'])
def abastecer():
    produto = request.form['produto']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])
    validade = request.form['validade']
    df_temp = pd.DataFrame({'Produto': [produto], 'Quantidade': [quantidade], 'Preço Unitário (R$)': [preco], 'Validade': [validade]})
    global df_estoque
    df_estoque = pd.concat([df_estoque, df_temp], ignore_index=True)
    df_estoque.to_csv('estoque_geladeira.csv', index=False)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)