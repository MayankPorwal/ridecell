from math import radians, sin, cos, acos
from typing import List

from db import db


class ParkingModel(db.Model):
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String(10))
    cost = db.Column(db.Float)

    def __init__(self, name: str, latitude: float, longitude: float, status: str, cost: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.cost = cost

    @classmethod
    def find_by_parking_name(cls, name: str) -> "ParkingModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_available_parkings(cls, status: str) -> List["ParkingModel"]:
        return cls.query.filter_by(status=status).all()

    @classmethod
    def find_occupied_parkings(cls) -> List["ParkingModel"]:
        return cls.query.filter(ParkingModel.status != "Free").all()

    @classmethod
    def display_cost_of_parkings(cls) -> List["ParkingModel"]:
        return cls.query.with_entities(ParkingModel.name, ParkingModel.cost)

    @classmethod
    def find_by_address(cls, latitude: float, longitude: float) -> "ParkingModel":
        return cls.query.filter(ParkingModel.longitude >= longitude).filter(ParkingModel.latitude >= latitude).filter(
            ParkingModel.status == "Free"
        )

    @classmethod
    def find_all(cls) -> List["ParkingModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

