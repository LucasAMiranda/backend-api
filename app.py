from flask import Flask, jsonify, request, render_template
from flasgger import Swagger
from flask_cors import CORS 
from model.models import db, Vinho 
from schemas.config import config_by_name 
from sqlalchemy.exc import IntegrityError 

# Seleção de Configuração
config_name = 'development' 

app = Flask(__name__)
# Carrega a configuração
app.config.from_object(config_by_name[config_name]) 

CORS(app) 
# Configuração básica do Flasgger
swagger = Swagger(app)

db.init_app(app) 

# ===============================================
# ROTA PRINCIPAL: SERVIR O FRONTEND
# ===============================================
@app.route('/', methods=['GET'])
def index():
    """
    Endpoint para carregar a página principal (index.html).
    ---
    tags:
      - Frontend
    responses:
      200:
        description: Retorna a página HTML do gerenciamento de vinhos.
    """
    return render_template('index.html')


# ===============================================
# ENDPOINTS PARA VINHOS
# ===============================================

@app.route('/cadastrar_vinho', methods=['POST'])
def cadastrar_vinho():
    """
    Cadastrar um Novo Vinho
    ---
    tags:
      - Vinhos
    parameters:
      - in: body
        name: body
        schema:
          id: Vinho
          required:
            - nome_vinho
            - data_fabricacao
            - cidade_producao
          properties:
            nome_vinho:
              type: string
              description: Nome do vinho.
            data_fabricacao:
              type: string
              format: date
              description: Data de fabricação (YYYY-MM-DD).
            cidade_producao:
              type: string
              description: Cidade onde o vinho foi produzido.
    responses:
      201:
        description: Vinho cadastrado com sucesso.
      400:
        description: Requisição inválida, dados incompletos ou nome duplicado.
    """
    try:
        data = request.get_json()
        
        required_fields = ['nome_vinho', 'data_fabricacao', 'cidade_producao']
        if not data or not all(field in data for field in required_fields):
             return jsonify({'message': 'Dados de entrada incompletos. Todos os campos são obrigatórios.'}), 400

        novo = Vinho(
            nome_vinho=data['nome_vinho'], 
            data_fabricacao=data['data_fabricacao'],
            cidade_producao=data['cidade_producao']
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'message': 'Vinho cadastrado com sucesso!'}), 201

    except IntegrityError as e:
        db.session.rollback()
        vinho_nome = data.get('nome_vinho', 'Desconhecido')
        return jsonify({'message': f'Erro: O vinho "{vinho_nome}" já existe. O nome deve ser único.'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Erro inesperado ao cadastrar: {e}") 
        return jsonify({'message': f'Erro interno ao cadastrar vinho: {str(e)}'}), 400

@app.route('/buscar_vinhos', methods=['GET'])
def buscar_vinhos():
    """
    Listar Todos os Vinhos
    ---
    tags:
      - Vinhos
    responses:
      200:
        description: Retorna uma lista de todos os vinhos cadastrados.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID único do vinho.
              nome_vinho:
                type: string
                description: Nome do vinho.
              data_fabricacao:
                type: string
                description: Data de fabricação (YYYY-MM-DD).
              cidade_producao:
                type: string
                description: Cidade de produção.
    """
    vinhos = Vinho.query.all()
    resultado = [
        {'id': v.id, 'nome_vinho': v.nome_vinho, 'data_fabricacao': v.data_fabricacao, 'cidade_producao': v.cidade_producao} 
        for v in vinhos
    ]
    return jsonify(resultado), 200


@app.route('/deletar_vinho/<int:id>', methods=['DELETE'])
def deletar_vinho(id):
    """
    Deletar Vinho por ID
    ---
    tags:
      - Vinhos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do vinho a ser deletado.
    responses:
      200:
        description: Vinho deletado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Vinho deletado com sucesso.
      404:
        description: Vinho não encontrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Vinho não encontrado.
    """
    vinho = Vinho.query.get(id)
    if vinho:
        db.session.delete(vinho)
        db.session.commit()
        return jsonify({'message': 'Vinho deletado com sucesso.'}), 200
    return jsonify({'message': 'Vinho não encontrado.'}), 404


if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas
        db.create_all() 
    app.run(debug=True)