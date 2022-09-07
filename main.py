from flask import Flask, redirect, request, render_template
from Exceptions import Exceptions
from Schools import School
from Helpers import Helpers

app = Flask(__name__)


@app.route("/lookup")
def lookup():
    try:
        address = request.args.get("address")

        if address:
            address_data = Helpers.address_data(address)
            weather = Helpers.get_weather(lat=address_data["lat"], lng=address_data["lng"])
            listings = Helpers.get_listings(address_data["formatted_address"])
            house_data = Helpers.get_house_data(listings)
            property_region = "Atlanta" if "GA" in address else "Asheville"
            distances = Helpers.get_distance_from(lat=address_data["lat"], lng=address_data["lng"], property_region=property_region)
            return render_template("results.html", weather=weather, address=address_data, listings=listings,
                                   house_data=house_data, distances=distances)

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