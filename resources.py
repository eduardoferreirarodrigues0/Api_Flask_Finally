from flask_restful import Resource, request
from flask import jsonify
from models import db, Motorista, Veiculo,Rota, MotoristaSchema, VeiculoSchema,RotaSchema

class MotoristaResource(Resource):
    #Cadastro de motorista
    def post(self):
        data = request.json
        motorista = Motorista(nome_motorista=data['nome_motorista'], idade_motorista=data['idade_motorista'], capacitacoes=data['capacitacoes'])
        db.session.add(motorista)
        db.session.commit()
        return MotoristaSchema().dump(motorista),201
    
    #Listagem de motorista
    def get(self, motorista_id=None):
        if motorista_id is None:
            motoristas = Motorista.query.all()
            return MotoristaSchema(many=True).dump(motoristas)
        
        motorista = Motorista.query.get(motorista_id)
        if not motorista:
            return {"message": "Motorista não encontrado"}, 404
        return MotoristaSchema().dump(motorista)

    
    #Alteração de motorista
    def put(self, motorista_id):
        motorista = Motorista.query.get(motorista_id)
        if not motorista:
            return {"message": "Motorista não encontrado"}, 404

        data = request.json
        motorista.nome_motorista = data.get('nome_motorista', motorista.nome_motorista)
        motorista.idade_motorista = data.get('idade_motorista', motorista.idade_motorista)
        motorista.capacitacoes = data.get('capacitacoes', motorista.capacitacoes)

        db.session.commit()

        return MotoristaSchema().dump(motorista)
    
    #Exclusão de motorista
    def delete(self, motorista_id):
        motorista = Motorista.query.get(motorista_id)
        if not motorista:
            return {"message": "Motorista não encontrado"}, 404
        
        db.session.delete(motorista)
        db.session.commit()

        return {"message": "Motorista excluído com sucesso"}, 204

    #Função para verificar se o motorista pode conduzir o veículo
    def pode_conduzir(self, motorista_id, categoria_veiculo):
        motorista = Motorista.query.get(motorista_id)
        
        if not motorista:
            return False
        
        capacidades_motorista = motorista.capacitacoes.split(',')  # Exemplo: "1,2"
        return str(categoria_veiculo) in capacidades_motorista


class VeiculoResource(Resource):
    #Cadastro de veículo
    def post(self):
        data = request.json
        motorista_id = data['motorista_id']
        categoria_veiculo = data['categoria_veiculo']
        
        motorista_resource = MotoristaResource()

        if not motorista_resource.pode_conduzir(motorista_id, categoria_veiculo):
            return {"message": "Motorista não capacitado para conduzir esse veículo"}, 400

        veiculo = Veiculo(
            categoria_veiculo=categoria_veiculo,
            placa_veiculo=data['placa_veiculo'],
            motorista_id=motorista_id,
            capacidade_veiculo=data['capacidade_veiculo']
        )

        db.session.add(veiculo)
        db.session.commit()

        return VeiculoSchema().dump(veiculo), 201
        
    #Listagem de veículo
    def get(self, veiculo_id=None):
        if veiculo_id is None:
            veiculos = Veiculo.query.all()
            return VeiculoSchema(many=True).dump(veiculos)
            
        veiculo = Veiculo.query.get(veiculo_id)
        if not veiculo:
            return {"message": "Veículo não encontrado"}, 404
        return VeiculoSchema().dump(veiculo)
    
    #Alteração de veículo
    def put(self, veiculo_id):
        veiculo = Veiculo.query.get(veiculo_id)
        if not veiculo:
            return {"message": "Veículo não encontrado"}, 404

        data = request.json
        categoria_veiculo = data.get('categoria_veiculo', veiculo.categoria_veiculo)
        motorista_id = data.get('motorista_id', veiculo.motorista_id)

        if not self.pode_conduzir(motorista_id, categoria_veiculo):
            return {"message": "Motorista não capacitado para conduzir esse veículo"}, 400

        veiculo.categoria_veiculo = categoria_veiculo
        veiculo.placa_veiculo = data.get('placa_veiculo', veiculo.placa_veiculo)
        veiculo.motorista_id = motorista_id
        veiculo.capacidade_veiculo = data.get('capacidade_veiculo', veiculo.capacidade_veiculo)

        db.session.commit()

        return VeiculoSchema().dump(veiculo)
    
    #Exclusão de veículo
    def delete(self, veiculo_id):
        veiculo = Veiculo.query.get(veiculo_id)
        if not veiculo:
            return {"message": "Veículo não encontrado"}, 404

        # Verifica se o veículo está vinculado a alguma rota
        if veiculo.rotas:
            return {"message": "Este veículo está vinculado a uma rota. Exclua a rota primeiro."}, 400

        db.session.delete(veiculo)
        db.session.commit()

        return {"message": "Veículo excluído com sucesso"}, 204

class RotaResource(Resource):
    #Cadastro de rota
    def atende_lotacao(self, capacidade_veiculo, lotacao_rota):
        return capacidade_veiculo >= lotacao_rota

    def post(self):
        data = request.json
        # Verifique se já existe uma rota com o mesmo veículo e turno
        veiculo_id = data['veiculo_id']
        turno = data['turno']

        rota_existente = Rota.query.filter_by(veiculo_id=veiculo_id, turno=turno).first()
        if rota_existente:
            return {"message": "Este veículo já está atribuído a uma rota no mesmo turno."}, 400

        rota = Rota(nome_rota=data['nome_rota'], distancia_rota=data['distancia_rota'], lotacao=data['lotacao'], turno=data['turno'], veiculo_id=data['veiculo_id'])
        db.session.add(rota)
        db.session.commit()
        return RotaSchema().dump(rota)
    
    #Listagem de rota
    def get(self, rota_id=None):
        if rota_id is None:
            rotas = Rota.query.all()
            return RotaSchema(many=True).dump(rotas)
            
        rota = Rota.query.get(rota_id)
        if not rota:
            return {"message": "Rota não encontrada"}, 404
        return RotaSchema().dump(rota)
    
    #Alteração de rota
    def put(self, rota_id):
        rota = Rota.query.get(rota_id)
        if not rota:
            return {"message": "Rota não encontrada"}, 404

        data = request.json
        rota.nome_rota = data.get('nome_rota', rota.nome_rota)
        rota.distancia_rota = data.get('distancia_rota', rota.distancia_rota)
        rota.lotacao = data.get('lotacao', rota.lotacao)
        rota.turno = data.get('turno', rota.turno)
        rota.veiculo_id = data.get('veiculo_id', rota.veiculo_id)

        db.session.commit()

        return RotaSchema().dump(rota)
    
    #Exclusão de rota
    def delete(self, rota_id):
        rota = Rota.query.get(rota_id)
        if not rota:
            return {"message": "Rota não encontrada"}, 404
        
        db.session.delete(rota)
        db.session.commit()

        return {"message": "Rota excluída com sucesso"}, 204
    
    #Função para verificar se o veículo atende a lotação da rota
    def atende_lotacao(self, veiculo_id, rota_id):
        veiculo = Veiculo.query.get(veiculo_id)
        rota = Rota.query.get(rota_id)
        
        if not veiculo:
            return False
        if not rota:
            return False
        
        return veiculo.capacidade_veiculo >= rota.lotacao_rota
