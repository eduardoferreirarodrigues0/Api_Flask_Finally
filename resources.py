from flask_restful import Resource, request
from flask import jsonify
from models import db, Motorista, Veiculo,Rota, MotoristaSchema, VeiculoSchema,RotaSchema

class MotoristaResource(Resource):
    def post(self):
        data = request.json
        motorista = Motorista(nome_motorista=data['nome_motorista'], idade_motorista=data['idade_motorista'])
        db.session.add(motorista)
        db.session.commit()
        return MotoristaSchema().dump(motorista),201
    
    def get(self, motorista_id=None):
        if motorista_id is None:
            motoristas = Motorista.query.all()
            return jsonify(MotoristaSchema(many=True).dump(motoristas))
        
        motorista = Motorista.query.get(motorista_id)
        if not motorista:
            return jsonify({"message": "Motorista não encontrado"}), 404
        return jsonify(MotoristaSchema().dump(motorista))

class VeiculoResource(Resource):
    def post(self):
        data = request.json
        veiculo = Veiculo(categoria_veiculo=data['categoria_veiculo'], placa_veiculo=data['placa_veiculo'], motorista_id=data['motorista_id'])
        db.session.add(veiculo)
        db.session.commit()
        return jsonify(VeiculoSchema().dump(veiculo))
    

    def get(self, veiculo_id=None):
        if veiculo_id is None:
            veiculos = Veiculo.query.all()
            return jsonify(VeiculoSchema(many=True).dump(veiculos))
            
        veiculo = Veiculo.query.get(veiculo_id)
        if not veiculo:
            return jsonify({"message": "Veículo não encontrado"}), 404
        return jsonify(VeiculoSchema().dump(veiculo))

class RotaResource(Resource):
    def post(self):
        data = request.json
        rota = Rota(nome_rota=data['nome_rota'], distancia_rota=data['distancia_rota'])
        db.session.add(rota)
        db.session.commit()
        return jsonify(RotaSchema().dump(rota))
    
    def get(self, rota_id=None):
        if rota_id is None:
            rotas = Rota.query.all()
            return jsonify(RotaSchema(many=True).dump(rotas))
            
        rota = Rota.query.get(rota_id)
        if not rota:
            return jsonify({"message": "Rota não encontrada"}), 404
        return jsonify(RotaSchema().dump(rota))