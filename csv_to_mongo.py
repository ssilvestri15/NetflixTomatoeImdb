import csv
from pymongo import MongoClient
from utils import *

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['netflixtomatoes']
collection = db['movies']

class Movie:
    def __init__(self, name, info, genres, directors, authors, release_date, runtime, production_company):
        self.name = name
        self.info = info
        self.genres = genres
        self.directors = directors
        self.authors = authors
        self.release_date = release_date
        self.runtime = runtime
        self.production_company = production_company

    @classmethod
    def create(self, name, release_date):
        return self(name, "", "", "", "", release_date, "", "")

    def greet(self):
        print(f"{self.name}, {self.release_date}")

rotten_movies_full = {}
rotten_movies_small = {}
netflix_movies = {}
imdb_movies = {}

missing_date = 0
with open('./dataset/rotten_tomatoes_movies.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Insert each row into MongoDB
        name = row['movie_title']
        info = row['movie_info']
        genres = row['genres']
        directors = row['directors']
        authors = row['authors']
        release_date = row['original_release_date']
        runtime = row['runtime']
        production_company = row['production_company']
        movie = Movie(name, info, genres, directors, authors, release_date, runtime, production_company)
        date = extract_year_from_date(movie.release_date)
        if date == "NA":
            missing_date += 1
        else:
            key = f"{name.lower()}_{date.lower()}"
            rotten_movies_full[key] = movie
            rotten_movies_small[key] = Movie.create(name.lower(), date.lower())

print(f"Number of rotten movies: {len(rotten_movies_full)} with {missing_date} missing dates")


inserted = 0
skip = 0
with open('./dataset/netflix_movies.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Insert each row into MongoDB
        name = row['MovieTitle']
        release_date = row['ReleaseYear']

        if (release_date is None or release_date == ""):
            skip += 1
            continue

        key = f"{name.lower()}_{release_date.lower()}"
        netflix_movies[key] = Movie.create(name.lower(), date.lower())
        inserted += 1

        """
        movie = rotten_movies.get(key)

        if movie is not None:
            date = extract_year_from_date(movie.release_date)
            try:
                collection.insert_one(movie.__dict__)
                inserted += 1
            except:
                skip += 1
        else:
            skip += 1
        """
            
    print(f"Inserted {inserted} netflix movies into MongoDB")
    print(f"Skipped {skip} netflix movies")

inserted = 0
skip = 0
with open('./dataset/imdb_movies.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Insert each row into MongoDB
        name = row['name']
        release_date = row['year']

        if (release_date is None or release_date == ""):
            skip += 1
            continue

        key = f"{name.lower()}_{release_date.lower()}"
        imdb_movies[key] = Movie.create(name.lower(), date.lower())
        inserted += 1

        """
        movie = rotten_movies.get(key)

        if movie is not None:
            date = extract_year_from_date(movie.release_date)
            try:
                collection.insert_one(movie.__dict__)
                inserted += 1
            except:
                skip += 1
        else:
            skip += 1
        """    
    print(f"Inserted {inserted} imdb movies into MongoDB")
    print(f"Skipped {skip} imdb movies")

# Find the intersection of the two dictionaries
def makeIntersection(dict1, dict2):
    intersection = set()
    for key in dict1:
        if key in dict2:
            intersection.add(key)
    return intersection

i1 = makeIntersection(rotten_movies_small, netflix_movies)
i2 = makeIntersection(i1, imdb_movies)

collection.insert_many([rotten_movies_full[key].__dict__ for key in i2])

# Print the intersection
print("Intersection based on 'name' and 'release_date':", len(i2))