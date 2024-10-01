from flask import Flask, jsonify, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

df_estoque = pd.read_csv('data/estoque_geladeira.csv')
df_status_geladeira = pd.read_csv('data/geladeira.csv')
temperatura = df_status_geladeira['Temperatura'].iloc[0]
porta = df_status_geladeira['Porta'].iloc[0]


@app.route('/')
def index():
    return render_template('index.html', estoque=df_estoque.to_dict(orient='records'), temperatura=temperatura, porta=porta)

@app.route('/geladeira')
def geladeira():
    
    temperatura = int(df_status_geladeira.loc[0, 'Temperatura'])
    porta = str(df_status_geladeira.loc[0, 'Porta'])
    return jsonify(temperatura=temperatura, porta=porta)

@app.route('/abastecer', methods=['POST'])
def abastecer():
    produto = request.form['produto']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])
    validade = request.form['validade']
    df_temp = pd.DataFrame({'Produto': [produto], 'Quantidade': [quantidade], 'Preço Unitário (R$)': [preco], 'Validade': [validade]})
    global df_estoque
    df_estoque = pd.concat([df_estoque, df_temp], ignore_index=True)
    df_estoque.to_csv('data/estoque_geladeira.csv', index=False)
    return redirect('/')

@app.route('/desabastecer', methods=['POST'])
def desabastecer():
    produto = request.form['produto']
    validade = request.form['validade']
    
    global df_estoque
    temp_produto = (df_estoque['Produto'] == produto) & (df_estoque['Validade'] == validade)
    
    if temp_produto.any():
        df_estoque = df_estoque[~temp_produto]
        df_estoque.to_csv('data/estoque_geladeira.csv', index=False)
        return redirect('/')
    else:
        # Tem que tretar com JS, modal, html, pra ter msg de erro na tela...
        return "Produto não encontrado - 404", 404

@app.route('/ajusta_temperatura', methods=['POST'])
def ajusta_temperatura():
    nova_temperatura = int(request.form['nova_temperatura'])
    if nova_temperatura < 9 and nova_temperatura > -3: 
        df_status_geladeira.at[0, 'Temperatura'] = nova_temperatura
        df_status_geladeira.to_csv('data/geladeira.csv', index=False)
        return redirect('/')
    else:
        return "Temperatura fora da faixa[-2°C a 8°C] - 400", 400

@app.route('/alterar_porta', methods=['POST'])
def alterar_porta():
    nova_situacao = request.form['nova_situacao']
    df_status_geladeira.at[0, 'Porta'] = nova_situacao
    df_status_geladeira.to_csv('data/geladeira.csv', index=False)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)