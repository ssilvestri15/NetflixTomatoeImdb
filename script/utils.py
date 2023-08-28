from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['netflixtomatoes']
movies_collection = db['movies']
netflix_collection = db["netflix_ratings"]
netflix_collection_real = db["netflix_ratings_real"]
tv_shows_collection = db["tv_shows"]

class MovieInfo:
    def __init__(self, id, score = 0):
        self.id = id
        self.num = score

class Movie:
    def __init__(self, name, info, genres, directors, authors, release_date, runtime, production_company, ratings):
        self.name = name
        self.info = info
        self.genres = genres
        self.directors = directors
        self.authors = authors
        self.release_date = release_date
        self.runtime = runtime
        self.production_company = production_company
        self.ratings = ratings

    @classmethod
    def create(self, name, release_date):
        return self(name, "", "", "", "", release_date, "", "", {})

    def greet(self):
        print(f"{self.name}, {self.release_date}")

def extract_year_from_date(date_string):

    if date_string is None or date_string == "":
        return "NA"

    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")  # Assuming the format is "YYYY-MM-DD"
    except ValueError:
        print("Invalid date format. Please provide a date string in the format 'YYYY-MM-DD'.")
        return None

    # Extract the year from the datetime object
    year = date_object.year.__str__()

    return year

def makeIntersection(dict1, dict2):
    intersection = set()
    for key in dict1:
        if key in dict2:
            intersection.add(key)
    return intersection