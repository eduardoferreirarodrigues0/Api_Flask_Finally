from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

class Motorista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_motorista = db.Column(db.String(100), nullable=False)
    categoria_motorista = db.Column(db.Integer)
    transportes = db.relationship('Transporte', backref='motorista', lazy=True)

class Transporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria_transporte = db.Column(db.Integer)
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'), nullable=False)

class Rota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_rota = db.Column(db.String(100), nullable=False)
    transportes_rota = db.relationship('Transporte', backref='rota', lazy=True)



class MotoristaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_motorista','categoria_motorista', 'trnasportes')

class TransporteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'categoria_transporte', 'motorista_id')

class RotaSchema(ma.Schema):
    class Meta:
        fields:('id','name_rota','transporte_rota')