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
from flask_cors import CORS # Permite a conexão do formulário de cadastro com a API  
import json
import os

app = Flask(__name__) # servidor que hospedará a API 
CORS(app)

ARQUIVO_LIVROS = "livros.txt" # constante que víncula o arquivo utilizado 

# Função para carregar livros do TXT
def carregar_livros():
    if not os.path.exists(ARQUIVO_LIVROS): # verificando se o arquivo existe no diretório
        return []

    with open(ARQUIVO_LIVROS, "r", encoding="utf-8") as arquivo: # faz a leitura do arquivo 
        return json.load(arquivo)

# Função para salvar livros no TXT
def salvar_livros(lista_livros):
    with open(ARQUIVO_LIVROS, "w", encoding="utf-8") as arquivo: 
        # Converte a lista de livros para o formato JSON e salva dentro do arquivo.
        # ensure_ascii=False permite salvar acentos corretamente.
        # indent=4 formata o arquivo com espaçamento para ficar mais legível.
        json.dump(lista_livros, arquivo, ensure_ascii=False, indent=4)

# Carrega livros ao iniciar a API
livros = carregar_livros()

# Função para gerar próximo ID
def gerar_proximo_id():
    if not livros:
        return 1
    return max(livro["id"] for livro in livros) + 1

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
    return jsonify({"erro": "Livro não encontrado"}), 404



# Editar um livro(ID)
@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):

    livro_alterado = request.get_json()   # Pega os novos dados enviados pelo usuário no corpo da requisição
    for indice,livro in enumerate(livros): # enumerate permite pegar o índice e o conteúdo da lista
        if livro.get('id') == id: # Verifica se encontrou o livro com o ID solicitado
            livros[indice].update(livro_alterado) # Atualiza os dados do livro com os novos valores enviados
            salvar_livros(livros) # salva os livros no arquivo 
            return jsonify(livros[indice])

    return jsonify({"erro": "Livro não encontrado"}), 404

# Criar (POST)
@app.route('/livros',methods=['POST'])
def incluir_novo_livro():
    dados = request.get_json()
    novo_livro = {
        "id": gerar_proximo_id(),
        "titulo": dados.get("titulo"),
        "autor": dados.get("autor")
    }

    livros.append(novo_livro)
    salvar_livros(livros)
    return jsonify(novo_livro), 201 

# Excluir (Delete)
@app.route('/livros/<int:id>',methods=['DELETE'])
def excluir_livro(id):
    for livro in livros:
        if livro["id"] == id:
            livros.remove(livro)
            salvar_livros(livros)
            return jsonify({"mensagem": "Livro removido com sucesso"})

    return jsonify({"erro": "Livro não encontrado"}), 404

        
# port -> porta onde a API vai rodar
# host -> endereço onde a API ficará disponível
# debug -> mostra erros detalhados durante desenvolvimento
app.run(port=5000, host='localhost', debug=True) 
    


