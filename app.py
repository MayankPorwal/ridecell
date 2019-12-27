from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.parking import (
     Parking,
     ParkingList,
     ParkingByStatus,
     ReserveParking,
     OccupiedParkings,
     CancelParking,
     ParkingCost,
     FindParkingByAddress
     )

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = 'my super secret key'.encode('utf8')  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(Parking, "/parking/<string:name>")
api.add_resource(ParkingList, "/parkings")
api.add_resource(ParkingByStatus, "/parkings_by_status/<string:status>")
api.add_resource(ReserveParking, "/reserve_parking/<string:name>")
api.add_resource(OccupiedParkings, "/occupied_parkings")
api.add_resource(CancelParking, "/cancel_parking/<string:name>")
api.add_resource(ParkingCost, "/parking_cost")
api.add_resource(FindParkingByAddress, "/nearby_parkings")


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
