from flask import Flask, redirect, request, render_template
from Exceptions import Exceptions
from Schools import School
from Helpers import Helpers
import requests

app = Flask(__name__)


@app.route("/lookup")
def lookup():
    try:
        address = request.args.get("address")

        if address:
            address_data = Helpers.address_data(address)
            weather = Helpers.get_weather(lat=address_data["lat"], lng=address_data["lng"])



            home_data = Helpers.address_data_refactor(address)
            return render_template("results.html", weather=weather, listings=[], house_data=home_data)

        else:
            raise Exceptions.MissingArgumentsException(missing_args=request.args)

    except Exceptions.MissingArgumentsException as e:
        return {
            "error": str(e),
            "status_code": 500
        }

@app.route("/saved")
def saved():

    return render_template()



#CLIMATE ROUTES
@app.route("/get_weather")
def get_weather():
    try:
        if request.args.get("lat") and request.args.get("lng"):
            lat = request.args.get("lat")
            lng = request.args.get("lng")
            weather = Helpers.get_climate(lat=lat, lng=lng)
            return weather
        else:
            raise Exceptions.MissingArgumentsException(missing_args=request.args)

    except Exceptions.MissingArgumentsException as e:
        return {
            "error": str(e),
            "status_code": 500
        }


#SCHOOL ROUTES
@app.route("/get_schools")
def get_schools():
    """
    Returns a list of schools and their attributes for a given location defined by Lat and Lng
    Raises: Exceptions.MissingArgumentsException when missing required args
    """
    try:

        if request.args.get("lat") and request.args.get("lng"):
            lat = request.args.get("lat")
            lng = request.args.get("lng")
            nearby_schools = Helpers.get_nearby_schools(lat=lat, lng=lng)
            return nearby_schools

        else:
            raise Exceptions.MissingArgumentsException(missing_args=["Lat, Lng"])

    except Exceptions.MissingArgumentsException as e:
        return {
            "error": str(e),
            "status_code": 500
        }


#DISTANCE ROUTES
@app.route("/get_distance_from")
def get_distance_from():
    try:
        if request.args.get("lat") and request.args.get("lng"):
            lat = request.args.get("lat")
            lng = request.args.get("lng")
            pois = Helpers.get_distance_from(lat, lng)
            return pois
        else:
            raise Exceptions.MissingArgumentsException(missing_args=request.args)

    except Exceptions.MissingArgumentsException as e:
        return {
            "error": str(e),
            "status_code": 500
        }




if __name__ == '__main__':
    app.run(debug=True)