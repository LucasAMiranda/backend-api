from flask_sqlalchemy import SQLAlchemy  

db = SQLAlchemy()

class Vinho(db.Model):
    # ID como chave primária
    id = db.Column(db.Integer, primary_key=True)
    
    # Detalhes do Vinho
    nome_vinho = db.Column(db.String(100), unique=True, nullable=False)
    data_fabricacao = db.Column(db.String(10), nullable=False) # Armazenada como string (YYYY-MM-DD)
    cidade_producao = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Vinho {self.nome_vinho}>'
