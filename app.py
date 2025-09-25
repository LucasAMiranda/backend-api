from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from models import db, Usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
swagger = Swagger(app)

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    """
    Endpoint para cadastrar um novo usuário.
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        schema:
          id: Usuario
          required:
            - nome
            - email
          properties:
            nome:
              type: string
              description: Nome do usuário
            email:
              type: string
              description: E-mail do usuário
    responses:
      201:
        description: Usuário cadastrado com sucesso.
      400:
        description: Requisição inválida.
    """
    try:
        data = request.get_json()
        novo = Usuario(nome=data['nome'], email=data['email'])
        db.session.add(novo)
        db.session.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'message': f'Erro ao cadastrar usuário: {str(e)}'}), 400
        

@app.route('/buscar_usuarios', methods=['GET'])
def buscar_usuarios():
    """
    Endpoint para listar todos os usuários.
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários.
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              nome:
                type: string
              email:
                type: string
      404:
        description: Nenhum usuário encontrado.
    """
    usuarios = Usuario.query.all()
    if usuarios:
        resultado = [{'id': u.id, 'nome': u.nome, 'email': u.email} for u in usuarios]
        return jsonify(resultado), 200
    else:
        return jsonify({'message': 'Nenhum usuário encontrado.'}), 404

@app.route('/buscar_usuario/<int:id>', methods=['GET'])
def buscar_usuario_por_id(id):
    """
    Endpoint para buscar um usuário por ID.
    ---
    tags:
      - Usuários
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Detalhes do usuário.
        schema:
          id: UsuarioDetalhe
          properties:
            id:
              type: integer
            nome:
              type: string
            email:
              type: string
      404:
        description: Usuário não encontrado.
    """
    usuario = Usuario.query.get(id)
    if usuario:
        return jsonify({'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado.'}), 404

@app.route('/deletar_usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    """
    Endpoint para deletar um usuário.
    ---
    tags:
      - Usuários
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do usuário a ser deletado.
    responses:
      200:
        description: Usuário deletado com sucesso.
      404:
        description: Usuário não encontrado.
    """
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário deletado com sucesso.'}), 200
    return jsonify({'message': 'Usuário não encontrado.'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

