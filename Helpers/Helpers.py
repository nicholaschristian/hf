import requests, json
from Schools import School
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


def get_request(fetch_url: str, as_json=False):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
    }
    r = requests.get(fetch_url, headers=headers)
    r.raise_for_status()
    if as_json:
        return r.json()
    return r.content


def post_request(fetch_url: str, payload: dict = None, as_json=True):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
    }
    r = requests.post(fetch_url, headers=headers, data=payload)
    r.raise_for_status()

    if as_json:
        return r.json()
    return r.content


def address_data(address: str, components: str = None):
    __components = address.split(",")
    street_address = __components[0].upper().replace(" ", "%20")
    address_data = get_request(
        f"https://maps.googleapis.com/maps/api/geocode/json?address={street_address}&key=AIzaSyBzU-uDQGLkMr9LOUm5eslzB_aVJNiAIGI",
        as_json=True)

    coordinate_data = address_data["results"][0]["geometry"]["location"]
    return {
        "formatted_address": address_data["results"][0]["formatted_address"],
        "house_number": __components[0],
        "lat": coordinate_data["lat"],
        "lng": coordinate_data["lng"]
    }

    return address_data


def get_weather(lat, lng) -> dict:
    try:
        weather_data = get_request(
            f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lng}&appid=4581483c219e73a362258da9030a8448&exclude=minutely,hourly,daily,alerts&units=imperial",
            as_json=True)
        return weather_data
    except Exception as e:
        return {
            "error": str(e)
        }


def get_nearby_schools(lat, lng):
    # TODO: Finish making post request

    nearby_schools = post_request("", payload=None)
    schools = [School.School(**school).__dict__() for school in nearby_schools]
    return schools


def get_distance_from(lat, lng, property_region):
    """
    Loads a list of defined POIs from txt file into memory.
    Iterates through each POI to calculate distance before adding to list and
    returning
    """

    def __load_pois():
        """
        Loads interests.json
        """

        pois_completed = []
        with open("/Users/nicholasyoung/Desktop/homefinder_api/Helpers/interests.json") as f:
            return json.load(f)

    def distance_matrix(place_ids, coordinates):
        """
        Returns Google data for distance between [place_ids] and given coordinates
        """
        place_ids = "|".join(place_ids)
        matrix_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={place_ids}&origins={coordinates['lat']},{coordinates['lng']}&key=AIzaSyBzU-uDQGLkMr9LOUm5eslzB_aVJNiAIGI&units=imperial"

        __results = get_request(matrix_url, as_json=True)
        results = []
        for location in __results["rows"][0]["elements"]:
            results.append(location)

        return results

    pois = __load_pois()

    # BELOW LOOP EXTRACTS AND CREATES THE PLACEID ARGUMENT FOR GOOGLE API REQUEST
    for region in pois:
        if property_region == region["region"]:
            locations = region["locations"]
            place_ids = ["place_id:" + location["placeID"] for location in locations]

    if place_ids:
        results = distance_matrix(place_ids=place_ids, coordinates={"lat": lat, "lng": lng})

        compiled = []
        for region in pois:
            if property_region == region["region"]:
                locations = region["locations"]

                for idx, location in enumerate(locations):
                    location["distance_matrix"] = (results[idx])

                return region



def get_listings(formatted_address: str):
    house_number = formatted_address.split(" ")[0]
    search_listings = ["zillow", "redfin", "realtor", "trulia"]
    gresults = get_request(f"https://www.google.com/search?q={formatted_address}+{'+'.join(search_listings)}")
    soup = BeautifulSoup(gresults, "html.parser")
    results = []
    for a in soup.findAll("a", href=True):

        for search_listing in search_listings:
            if search_listing + ".com" in a["href"] and house_number in a["href"]:
                listing = {
                    "source": search_listing.upper(),
                    "link": a["href"]
                }
                results.append(listing)
    return results


def get_house_data(listing_results):
    """
    Returns generic house data. bed, bath, sqft
    """

    for listing in listing_results:
        if listing["source"] == "TRULIA":
            page_data = get_request(listing["link"])
            soup = BeautifulSoup(page_data, "html.parser")
            results = soup.findAll(class_="MediaBlock__MediaContent-skmvlj-1")
            house = {}
            idx = 0
            for result in results:

                if "Beds" in result.getText():
                    print(result.getText())
                    house["beds"] = result.getText()
                if "Baths" in result.getText():
                    house["baths"] = result.getText()
                if "sqft" in result.getText():
                    house["sqft"] = result.getText()
                idx += 1

            return house
    return {
        "beds": "n/a",
        "baths": "n/a",
        "sqft": "n/a"
    }



