from flask_restful import Resource, request
from marshmallow import ValidationError
from models.item import ItemModel
from schemas.item import ItemSchema

NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the item."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."
ITEMS_DELETED = "Items deleted."

item_schema = ItemSchema()


class Item(Resource):
    @classmethod
    def get(cls, name: str, key: str):
        item = ItemModel.find_by_name_and_key(name, key)
        if item:
            return item_schema.dump(item), 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def delete(cls, name: str, key: str):
        item = ItemModel.find_by_name_and_key(name, key)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}, 200

        return {"message": ITEM_NOT_FOUND}, 404


class ItemPost(Resource):
    @classmethod
    def post(cls, name: str, key: str, text: str):
        item_json = request.get_json()
        item_json["name"] = name
        item_json["key"] = key
        item_json["text"] = text

        if ItemModel.find_by_name_and_key(name, key):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        try:
            item = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item_schema.dump(item), 201

    @classmethod
    def put(cls, name: str, key: str, text: str):
        item_json = request.get_json()
        item = ItemModel.find_by_name_and_key(name, key)

        if item:
            item_json["text"] = text
            item.text = item_json["text"]
        else:
            item_json["name"] = name
            item_json["key"] = key
            item_json["text"] = text

            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 400

        item.save_to_db()

        return item_schema.dump(item), 200
