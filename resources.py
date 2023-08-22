from flask_restful import Resource, reqparse
from flask import jsonify
from models import db, Motorista, Transporte,Rota, MotoristaSchema, TransporteSchema,RotaSchema

class MotoristaResource(Resource):
    def get(self,motorista_id=None):
        if motorista_id is None:
            motoristas = Motorista.query.all()
            return MotoristaSchema(many=True).dump(motoristas), 200
        
        motorista = Motorista.query.get(motorista_id)
        return MotoristaSchema().dump(motorista), 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome_motorista', type=str, required=True)
        args = parser.parse_args()
        
        motorista = Motorista(name=args['nome_motorista'])
        db.session.add(motorista)
        db.session.commit()
        
        return MotoristaSchema().dump(motorista), 201
    
class TransporteResource(Resource):
    def get(self,trnasporte_id):
        transporte = Transporte.query.get(transporte_id)
        return TransporteSchema().dump(transporte), 200