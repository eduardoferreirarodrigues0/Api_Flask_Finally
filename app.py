from flask import Flask
from flask_restful import Api
from models import db, ma
from resources import MotoristaResource, TransporteResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)
ma.init_app(app)



with app.app_context():
    db.create_all()

api.add_resource(MotoristaResource, '/motorista', '/mototrista/<int:motorista_id>')
api.add_resource(TransporteResource, '/transporte/<int:transporte_id>')

if __name__ == '__main__':
    app.run(debug=True)