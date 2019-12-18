from typing import List

from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    text = db.Column(db.String)
    key = db.Column(db.String, nullable=False)

    @classmethod
    def find_by_name_and_key(cls, name: str, key: str) -> "ItemModel":
        return cls.query.filter_by(name=name).filter_by(key=key).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
