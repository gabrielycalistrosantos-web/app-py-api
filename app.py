# API - Lugar para disponibiizar recursos e/ou funcionalidades
# 1. Objetivo da API - criar uma API que disponibiliza a consulta, criação, alteração e exclusão de livros
# 2. URL base - local para o qual serão feitas as requisições 
# URL - localhost
# 3. Endpoints - Quais são as funcionalidades disponibilizadas
    # - localhost/livros(GET) / obter todos os livros
    # - localhost/livros/id (GET) / obter livros por ID 
    # - localhost/livros/id (PUT) / modificar um livro específico
    # - localhost/livros (POST) / criar um livro
    # - localhost/livros/id (DELETE) / deletar um livro específico
# 4. Quais recursos ou funcionalidades - Livros

# API criada com Flask 

from flask import Flask, jsonify, request # flask - servidor/ jsonify - formato Json esperado de uma API/ request - permite o acesso aos dados

app = Flask(__name__) # servidor que hospedará a API 

# Criando a fonte de dados
# (Aqui estamos usando uma lista em memória ao invés de banco de dados)

livros = [
   {
       'id': 1,
       'título': 'O senhor dos Anéis',
       'autor': 'J.R.R Tolkien'
   },
   {
       'id': 2,
       'título': 'A culpa é das estrelas',
       'autor': 'John Green'
   },
   {
       'id': 3,
       'título': 'O menino do pijama listrado',
       'autor': 'John Boyne'
   },
]

# Consultar(todos)
@app.route('/livros', methods=['GET']) # garantir que somente o método GET seja aceito dentro dessa requisição
def obter_livros():
    return jsonify(livros)  # Retorna a lista completa de livros em formato JSON

# Consultar(individual - ID)
@app.route('/livros/<int:id>', methods=['GET']) # <int:id> -> recebe um número na URL
def obter_livros_id(id):
    for livro in livros: # Percorre a lista de livros procurando o ID informado
        if livro.get('id') == id: # Verifica se o ID do livro é igual ao ID recebido na URL
            return jsonify(livro)  # Retorna o livro encontrado

# Editar um livro(ID)
@app.route('/livros/<int:id>',methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()   # Pega os novos dados enviados pelo usuário no corpo da requisição
    for indice,livro in enumerate(livros): # enumerate permite pegar o índice e o conteúdo da lista
        if livro.get('id') == id: # Verifica se encontrou o livro com o ID solicitado
            livros[indice].update(livro_alterado) # Atualiza os dados do livro com os novos valores enviados
            return jsonify(livros[indice])
        
# Criar (POST)
@app.route('/livros',methods=['POST'])
def incluir_novo_livro():
    novo_livro = request.get_json()  # Recebe os dados enviados pelo usuário
    livros.append(novo_livro) # Adiciona o novo livro na lista
    return jsonify(livros)  # Retorna a lista atualizada

# Excluir (Delete)
@app.route('/livros/<int:id>',methods=['DELETE'])
def excluir_livro(id):
    for indice, livro in enumerate(livros): # Percorre a lista para encontrar o livro pelo ID
        if livro.get('id') == id:
            del livros[indice]  # Remove o livro da lista
            return jsonify(livros)  # Retorna a lista atualizada
        
# port -> porta onde a API vai rodar
# host -> endereço onde a API ficará disponível
# debug -> mostra erros detalhados durante desenvolvimento
app.run(port=5000, host='localhost', debug=True) 
    


