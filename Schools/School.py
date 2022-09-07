class School:
    def __init__(self, **school_data):
        self.name = school_data.get("name")
        self.rating = school_data.get("rating")
        self.address = school_data.get("address ")

    def __dict__(self):
        return {
            "name": self.name,
            "rating": self.rating,
            "address": self.address
        }