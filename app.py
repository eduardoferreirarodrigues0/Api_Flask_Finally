from flask import Flask
from flask_restful import Api
from models import db, ma
from resources import MotoristaResource, VeiculoResource, RotaResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)
ma.init_app(app)

api.add_resource(MotoristaResource, '/cadastrar_motorista', '/cadastrar_motorista/<int:motorista_id>')
api.add_resource(VeiculoResource, '/cadastrar_veiculo', '/cadastrar_veiculo/<int:veiculo_id>')
api.add_resource(RotaResource, '/cadastrar_rota', '/cadastrar_rota/<int:rota_id>')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)