import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserLogin, UserRegister, User
from resources.item import Item, Item_List
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_NEW', 'sqlite:///data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTION"] = True
app.secret_key = 'tonycdsfdsgfDSDASDGEEWRTFWETWETGWGDG'
api = Api(app)


jwt = JWTManager(app) 


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # Instead of hard-coding, you should read from a config file or a database
        return {'is_admin': True}

    return {'is_admin': False}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Item_List, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == "__main__":
    db.init_app(app)
    
    @app.before_first_request
    def create_tables():
        db.create_all()
        
    app.run(port=5000, debug=True)


