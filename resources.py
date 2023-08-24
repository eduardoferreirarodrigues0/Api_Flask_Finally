from flask_restful import Resource, request, reqparse
from flask import jsonify
from models import db, Motorista, Veiculo,Rota, MotoristaSchema, VeiculoSchema,RotaSchema

class MotoristaResource(Resource):
    #Cadastro de motorista
    def post(self):
        data = request.json
        motorista = Motorista(nome_motorista=data['nome_motorista'], idade_motorista=data['idade_motorista'], tipo_veiculo_conduzido=data['tipo_veiculo_conduzido'])
        db.session.add(motorista)
        db.session.commit()
        return MotoristaSchema().dump(motorista),201
    
    #Listagem de motorista
    def get(self, motorista_id=None):
        if motorista_id is None:
            motoristas = Motorista.query.all()
            return jsonify(MotoristaSchema(many=True).dump(motoristas))
        
        motorista = Motorista.query.get(motorista_id)
        if not motorista:
            return jsonify({"message": "Motorista não encontrado"}), 404
        return jsonify(MotoristaSchema().dump(motorista))
    
    #Alteração de motorista
    def put(self, motorista_id):
        motorista = Motorista.query.get(motorista_id)
        if not motorista:
            return jsonify({"message": "Motorista não encontrado"}), 404

        data = request.json
        motorista.nome_motorista = data.get('nome_motorista', motorista.nome_motorista)
        motorista.idade_motorista = data.get('idade_motorista', motorista.idade_motorista)
        motorista.tipo_veiculo_conduzido = data.get('tipo_veiculo_conduzido', motorista.tipo_veiculo_conduzido)

        db.session.commit()

        return jsonify(MotoristaSchema().dump(motorista))
    
    #Exclusão de motorista
    def delete(self, motorista_id):
        motorista = Motorista.query.get(motorista_id)
        if not motorista:
            return jsonify({"message": "Motorista não encontrado"}), 404
        
        db.session.delete(motorista)
        db.session.commit()

        return jsonify({"message": "Motorista excluído com sucesso"}), 204

    #Função para verificar se o motorista pode conduzir o veículo
    def pode_conduzir(self, motorista_id, veiculo_id):
        motorista = Motorista.query.get(motorista_id)
        veiculo = Veiculo.query.get(veiculo_id)
        
        if not motorista:
            return False
        if not veiculo:
            return False
        
        capacidades_motorista = motorista.capacitacoes.split(',')  # Exemplo: "1,2"
        tipo_veiculo_veiculo = str(veiculo.categoria_veiculo)  # Exemplo: 1
        
        return tipo_veiculo_veiculo in capacidades_motorista


class VeiculoResource(Resource):
    #Cadastro de veículo
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('categoria_veiculo', type=int, required=True)
        parser.add_argument('placa_veiculo', type=str, required=True)
        parser.add_argument('motorista_id', type=int, required=True)
        args = parser.parse_args()
        
        motorista_id = args['motorista_id']
        veiculo = Veiculo(
            categoria_veiculo=args['categoria_veiculo'],
            placa_veiculo=args['placa_veiculo'],
            motorista_id=motorista_id
        )

        if not self.pode_conduzir(motorista_id, veiculo.categoria_veiculo):
            return jsonify({"message": "Motorista não capacitado para conduzir esse veículo"}), 400
        
        db.session.add(veiculo)
        db.session.commit()
        
        return VeiculoSchema().dump(veiculo), 201
    
    #Listagem de veículo
    def get(self, veiculo_id=None):
        if veiculo_id is None:
            veiculos = Veiculo.query.all()
            return jsonify(VeiculoSchema(many=True).dump(veiculos))
            
        veiculo = Veiculo.query.get(veiculo_id)
        if not veiculo:
            return jsonify({"message": "Veículo não encontrado"}), 404
        return jsonify(VeiculoSchema().dump(veiculo))
    
    #Alteração de veículo
    def put(self, veiculo_id):
        veiculo = Veiculo.query.get(veiculo_id)
        if not veiculo:
            return jsonify({"message": "Veículo não encontrado"}), 404

        data = request.json
        veiculo.categoria_veiculo = data.get('categoria_veiculo', veiculo.categoria_veiculo)
        veiculo.placa_veiculo = data.get('placa_veiculo', veiculo.placa_veiculo)
        veiculo.motorista_id = data.get('motorista_id', veiculo.motorista_id)
        veiculo.capacidade_veiculo = data.get('capacidade_veiculo', veiculo.capacidade_veiculo)


        db.session.commit()

        return jsonify(VeiculoSchema().dump(veiculo))
    
    #Exclusão de veículo
    def delete(self, veiculo_id):
        veiculo = Veiculo.query.get(veiculo_id)
        if not veiculo:
            return jsonify({"message": "Veículo não encontrado"}), 404
        
        db.session.delete(veiculo)
        db.session.commit()

        return jsonify({"message": "Veículo excluído com sucesso"}), 204

class RotaResource(Resource):
    #Cadastro de rota
    def atende_lotacao(self, capacidade_veiculo, lotacao_rota):
        return capacidade_veiculo >= lotacao_rota

    def post(self):
        data = request.json
        rota = Rota(nome_rota=data['nome_rota'], distancia_rota=data['distancia_rota'], lotacao=data['lotacao'])
        db.session.add(rota)
        db.session.commit()
        return jsonify(RotaSchema().dump(rota))
    
    #Listagem de rota
    def get(self, rota_id=None):
        if rota_id is None:
            rotas = Rota.query.all()
            return jsonify(RotaSchema(many=True).dump(rotas))
            
        rota = Rota.query.get(rota_id)
        if not rota:
            return jsonify({"message": "Rota não encontrada"}), 404
        return jsonify(RotaSchema().dump(rota))
    
    #Alteração de rota
    def put(self, rota_id):
        rota = Rota.query.get(rota_id)
        if not rota:
            return jsonify({"message": "Rota não encontrada"}), 404

        data = request.json
        rota.nome_rota = data.get('nome_rota', rota.nome_rota)
        rota.distancia_rota = data.get('distancia_rota', rota.distancia_rota)
        rota.lotacao = data.get('lotacao', rota.lotacao)

        db.session.commit()

        return jsonify(RotaSchema().dump(rota))
    
    #Exclusão de rota
    def delete(self, rota_id):
        rota = Rota.query.get(rota_id)
        if not rota:
            return jsonify({"message": "Rota não encontrada"}), 404
        
        db.session.delete(rota)
        db.session.commit()

        return jsonify({"message": "Rota excluída com sucesso"}), 204
    
    #Função para verificar se o veículo atende a lotação da rota
    def atende_lotacao(self, veiculo_id, rota_id):
        veiculo = Veiculo.query.get(veiculo_id)
        rota = Rota.query.get(rota_id)
        
        if not veiculo:
            return False
        if not rota:
            return False
        
        return veiculo.capacidade_veiculo >= rota.lotacao_rota
