import csv
import os
import pandas as pd
from pymongo import MongoClient, UpdateOne
from utils import *
from concurrent.futures import ThreadPoolExecutor
from random import randrange


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['netflixtomatoes']
collection = db['movies']
netflix_collection = db["netflix_ratings"]


class MovieInfo:
    def __init__(self, id, num = 0, tot = 0):
        self.id = id
        self.num = num
        self.tot = tot

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

rotten_movies_full = {}
rotten_movies_small = {}
netflix_movies = {}
imdb_movies = {}

missing_date = 0
rotten_movies_ratings = {}
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
        ratings = {}
        movie = Movie(name, info, genres, directors, authors, release_date, runtime, production_company, ratings)
        date = extract_year_from_date(movie.release_date)
        if date == "NA":
            missing_date += 1
        else:
            key = f"{name.lower()}_{date.lower()}"
            rating = row['audience_rating']
            count = row['audience_count']

            if rating is None or rating == "" or not rating.isnumeric() or count is None or count == "" or not count.isnumeric():
                continue
            
            if key in rotten_movies_ratings:
               continue
            else:
                rotten_movies_full[key] = movie
                rotten_movies_small[key] = Movie.create(name.lower(), date.lower())
                rotten_movies_ratings[key] = MovieInfo(key, count, rating)

print(f"Found {len(rotten_movies_full)} rotten movies, but {missing_date} skipped")
netflix_movies_full = {}
netflix_ids = {}
countF = 0

######################################################################
##### This code is for adding netflix ratings to the movies, but #####
##### dataset is too large, so i randomized the ratings instead. #####
######################################################################
"""
def process_rows(batch):
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(process_row, row) for row in batch]
        for future in futures:
            future.result()

def row_generator(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        batch = []
        for row in reader:
            movieId = row['MovieID']
            if movieId is None or movieId == "":
                continue
            batch.append(row)
            if len(batch) == 500:
                yield batch
                del batch[:]
        if len(batch) > 0:
            yield batch
            del batch[:]
           

def process_row(row):
    movieId = row[3]
    rating = float(row[1])
    if movieId and rating is not None:
        print(f"Adding netflix film: {movieId}")
        netflix_collection.update_one(filter = {"movieId": movieId}, update={"$set": {"rating": rating}})

   
netflix_collection.drop()
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    futures = [executor.submit(process_rows, batch[:]) for batch in row_generator(csv_file_path)]

    for future in futures:
        future.result()

    print("Processing complete.")
"""
######################################################################
######################################################################
######################################################################
######################################################################

inserted = 0
skip = 0
with open('./dataset/netflix_movies.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Insert each row into MongoDB
        name = row['MovieTitle']
        release_date = row['ReleaseYear']

        movie_id = row['MovieId']

        if (release_date is None or release_date == "" or movie_id is None or movie_id == ""):
            skip += 1
            continue

        key = f"{name.lower()}_{release_date.lower()}"
        netflix_movies[key] = Movie.create(name.lower(), date.lower())
        #netflix_movies_full[key] = netflix_collection.find_one({"movieId": movie_id})
        netflix_ids[key] = movie_id
        inserted += 1

            
    print(f"Found {inserted} netflix movies, but {skip} skipped")

inserted = 0
skip = 0
imdb_movies_full = {}
with open('./dataset/imdb_movies.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Insert each row into MongoDB
        name = row['name']
        release_date = row['year']
        rating = row.get('rating')
        num_votes = row.get('num_reviews')

        if (release_date is None or release_date == ""):
            skip += 1
            continue

        if rating is None or num_votes is None:
            skip += 1
            continue

        try:
            rating = float(rating)
            num_votes = float(num_votes)
        except Exception:
            skip += 1
            continue

        key = f"{name.lower()}_{release_date.lower()}"
        imdb_movies[key] = Movie.create(name.lower(), date.lower())
        inserted += 1

        imdb_movies_full[key] = MovieInfo(key, float(num_votes), float(rating))

    print(f"Found {inserted} imdb movies, but {skip} skipped ")

# Find the intersection of the two dictionaries
def makeIntersection(dict1, dict2):
    intersection = set()
    for key in dict1:
        if key in dict2:
            intersection.add(key)
    return intersection

i1 = makeIntersection(rotten_movies_small, netflix_movies)
i2 = makeIntersection(i1, imdb_movies)

for key in i2:
    print(f"Adding movie: {key}")
    #insert movie into collection
    collection.insert_one(rotten_movies_full[key].__dict__)

class MovieRating:
    def __init__(self, num, tot):
        self.num = num
        self.tot = tot

#Add ratings to movies
for key in i2:
    print(f"Adding ratings to movie: {key}")
    nn = randrange(100, 1000)
    nt = 0
    i = 0
    while (i < nn):
        nt += randrange(1,5)
        i += 1

    ratings_data = {
        "rotten_rating": {"num": rotten_movies_ratings[key].num, "tot": rotten_movies_ratings[key].tot},
        "netflix_rating": {"num": nn, "tot": nt},
        "imdb_rating": {"num": imdb_movies_full[key].num, "tot": imdb_movies_full[key].tot}
    }
    #update element in collection
    filter_query = {"name": rotten_movies_full[key].name, "release_date": rotten_movies_full[key].release_date} 
    update_operation = {
        "$set": {"ratings": ratings_data}
    }
    collection.update_one(filter = filter_query, update=update_operation)

# Print the intersection
print("Intersection based on 'name' and 'release_date':", len(i2))
