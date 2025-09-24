from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from models import db, Usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
swagger = Swagger(app)

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    novo_usuario = Usuario(nome=data['nome'], email=data['email'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201


@app.route('/buscar_usuarios/<int:id>', methods=['GET'])
def buscar_usuarios():
    if usuarios:
        usuarios = Usuario.query.all()
        resultado = [{'id': u.id, 'nome': u.nome, 'email': u.email} for u in usuarios]
        return jsonify(resultado), 200
    else:
        return jsonify({'message': 'Nenhum usuário encontrado.'}), 404
    
    
@app.route('deletar_usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário deletado com sucesso.'}), 404
    return jsonify({'message': 'Usuário não encontrado.'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

