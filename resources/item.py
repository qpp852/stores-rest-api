from sqlite3.dbapi2 import connect
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.orm import query
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type = float,
        required = True,
        help = "This field cannot be left blank."
    )
    parser.add_argument("store_id",
        type = int,
        required = True,
        help = "Eyery item needs a store id."
    )
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already existed."}, 400
        
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500 

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, **data)

        if not item:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message": "An error occured inserting the item."}, 500 
            
        else:
            try:
                item.price = data['price']
                # item.store_id = data['store_id']
            except:
                return {"message": "An error occured updating the item."}, 500 

        item.save_to_db()
        return item.json()
        

class Item_List(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}, 200