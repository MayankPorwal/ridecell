from flask import request
from flask_restful import Resource, reqparse

from marshmallow import ValidationError

from models.parking import ParkingModel
from schemas.parking import ParkingSchema

parking_schema = ParkingSchema()
parking_list_schema = ParkingSchema(many=True)


class Parking(Resource):
    @classmethod
    def get(cls, name: str):
        parking = ParkingModel.find_by_parking_name(name)
        if parking:
            return parking_schema.dump(parking), 200

        return {"message": "parking with this name not found!!"}, 404

    @classmethod
    def post(cls, name: str):
        if ParkingModel.find_by_parking_name(name):
            return {"message": "Parking by this name already exists"}, 400

        parking_json = request.get_json()
        parking_json["name"] = name

        try:
            parking_data = parking_schema.load(parking_json)
        except ValidationError as err:
            return err.messages, 400

        parking = ParkingModel(**parking_data)
        try:
            parking.save_to_db()
        except:
            return {"message": "Internal server error"}, 500

        return parking_schema.dump(parking), 201

    @classmethod
    def delete(cls, name: str):
        parking = ParkingModel.find_by_parking_name(name)
        if parking:
            parking.delete_from_db()
            return {"message": "Deleted parking spot successfully!!"}, 200

        return {"message": "Parking by this name already exists"}, 404

    @classmethod
    def put(cls, name: str):
        parking_json = request.get_json()
        parking = ParkingModel.find_by_parking_name(name)

        if parking:
            parking.latitude = parking_json["latitude"]
            parking.longitude = parking_json["longitude"]
            parking.status = parking_json["status"]
        else:
            parking_json["name"] = name

            try:
                parking_data = parking_schema.load(parking_json)
            except ValidationError as err:
                return err.messages, 400
            parking = ParkingModel(**parking_data)
        parking.save_to_db()

        return parking_schema.dump(parking), 200


class ParkingByStatus(Resource):
    @classmethod
    def get(cls, status: str):
        parking = ParkingModel.find_available_parkings(status)
        if parking:
            return parking_list_schema.dump(parking), 200

        return {"message": "No available parkings now!!"}, 404


class ReserveParking(Resource):
    @classmethod
    def post(cls, name: str):
        parking = ParkingModel.find_by_parking_name(name)

        if parking and parking.status == 'Free':
            parking.status = "Booked"
            parking.save_to_db()

        return parking_schema.dump(parking), 200


class OccupiedParkings(Resource):
    @classmethod
    def get(cls):
        parking = ParkingModel.find_occupied_parkings()

        if parking:
            return parking_list_schema.dump(parking), 200

        return {"message": "No occupied parkings now!!"}, 404


class CancelParking(Resource):
    @classmethod
    def post(cls, name: str):
        parking = ParkingModel.find_by_parking_name(name)

        if parking:
            parking.status = "Free"
            parking.save_to_db()

        return parking_schema.dump(parking), 200


class ParkingCost(Resource):
    @classmethod
    def get(cls):
        return {"parkings": parking_list_schema.dump(ParkingModel.display_cost_of_parkings())}, 200


class FindParkingByAddress(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('latitude')
    parser.add_argument('longitude')

    @classmethod
    def get(cls):
        args = FindParkingByAddress.parser.parse_args()
        latitude = args['latitude']  # List ['A', 'B']
        longitude = args['longitude']  # Boolean True
        return {"parkings": parking_list_schema.dump(ParkingModel.find_by_address(latitude, longitude))}, 200


class ParkingList(Resource):
    @classmethod
    def get(cls):
        return {"parkings": parking_list_schema.dump(ParkingModel.find_all())}, 200
