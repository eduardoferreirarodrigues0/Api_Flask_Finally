from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

class Motorista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_motorista = db.Column(db.String(100), nullable=False)
    idade_motorista = db.Column(db.Integer, nullable=False)
    capacitacoes = db.Column(db.String)  # Pode ser uma string com tipos de veículos (ex: "1,2")

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria_veiculo = db.Column(db.Integer, nullable=False)  # 1: Pequeno Porte, 2: Grande Porte
    placa_veiculo = db.Column(db.String(6), nullable=False)
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'), nullable=False)
    capacidade_veiculo = db.Column(db.Integer, nullable=False)

class Rota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_rota = db.Column(db.String(100), nullable=False)
    distancia_rota = db.Column(db.Float, nullable=False)
    lotacao = db.Column(db.Integer, nullable=False)
    turno = db.Column(db.String(50), nullable=False)  # Exemplo: "Manhã", "Tarde", "Noite"
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'))
    veiculo = db.relationship('Veiculo', backref='rotas')

class MotoristaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Motorista

    id = ma.auto_field()
    nome_motorista = ma.auto_field()
    idade_motorista = ma.auto_field()
    capacitacoes = ma.auto_field()

class VeiculoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Veiculo
        include_fk = True

    
    id = ma.auto_field()
    categoria_veiculo = ma.auto_field()
    placa_veiculo = ma.auto_field()
    motorista_id = ma.auto_field()
    capacidade_veiculo= ma.auto_field()

class RotaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rota
        include_fk = True
    
    id = ma.auto_field()
    nome_rota = ma.auto_field()
    distancia_rota = ma.auto_field()
    lotacao = ma.auto_field()
    turno = ma.auto_field()
    veiculo_id = ma.auto_field()

    