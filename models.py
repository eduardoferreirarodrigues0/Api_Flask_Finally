from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

class Motorista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_motorista = db.Column(db.String(100), nullable=False)
    idade_motorista = db.Column(db.Integer, nullable=False)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria_veiculo = db.Column(db.Integer, nullable=False)  # 1: Pequeno Porte, 2: Grande Porte
    placa_veiculo = db.Column(db.String(6), nullable=False)
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'), nullable=False)

class Rota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_rota = db.Column(db.String(100), nullable=False)
    distancia_rota = db.Column(db.Float, nullable=False)

class MotoristaSchema(ma.Schema):
    class meta:
        fields = ('id', 'nome_motorista', 'idade_motorista')

class VeiculoSchema(ma.Schema):
    class meta:
        fields = ('id', 'categoria_veiculo', 'placa_veiculo', 'motorista_id')

class RotaSchema(ma.Schema):
    class meta:
        fields = ('id', 'nome_rota', 'distancia_rota')