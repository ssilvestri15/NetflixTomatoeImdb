from utils import Movie, MovieInfo, netflix_collection, netflix_collection_real
import csv
import os

def getNetflixMovies():
    skip = 0
    netflix_movies = {}
    netflix_ids = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.abspath(os.path.join(script_dir, '..', 'dataset'))
    csv_path = os.path.join(dataset_dir, 'netflix_movies.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
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
            netflix_movies[key] = Movie.create(name.lower(), release_date.lower())
            netflix_ids[key] = movie_id
            
    print(f"Found {len(netflix_movies)} netflix movies, but {skip} skipped")
    return netflix_movies, netflix_ids

def getNetflixRating(movieId: int, key: str, pre_processed: bool = True):  

    if pre_processed:
        try:
            id = int(movieId)
            rating = netflix_collection_real.find_one({"MovieId": id})
            if rating is None:
                print(f"Could not find netflix rating for movie: {movieId}")
                return None
            rating = rating["Rating"]
            return MovieInfo(key, rating)
        except Exception as e:
            print(f"[P] Error: {e}")
            return None
    else:

        if netflix_collection.count_documents({}) == 0:
            print("######################################################################################################################################")
            print("# No netflix ratings collection found ################################################################################################")
            print("# Please run the following command to create the collection: #########################################################################")
            print("## mongoimport --db netflixtomatoes --collection netflix_ratings --type csv --file ../dataset/Netflix_User_Ratings.csv --headerline ##")
            print("# Then run the following command to create index under MovieId: ######################################################################")
            print("## db.netflix_ratings.createIndex({MovieId: 1}) ######################################################################################")
            print("######################################################################################################################################")
            return None
        
        try:
            id = int(movieId)
            result = list(netflix_collection.aggregate([
                { "$match": { "MovieId": id } },
                { "$group": {"_id": None, "total_sum": { "$sum": "$Rating" }, "count": { "$sum": 1 }}}
            ]))

            if result and len(result) > 0:
                total_sum = result[0]["total_sum"]
                count = result[0]["count"]
                rating = total_sum / count
                netflix_collection_real.insert_one({"MovieId": id, "Rating": rating, "Count": count, "Sum": total_sum})
                return MovieInfo(key, rating)
            else:
                print(f"Could not find netflix rating for movie: {movieId}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def insertNetflixPreProcessed():
    netflix_collection_real.drop()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.abspath(os.path.join(script_dir, '..', 'dataset'))
    csv_path = os.path.join(dataset_dir, 'netflix_ratings_real.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Insert each row into MongoDB
            try:
                name = row['MovieId']
                sum = row['Sum']
                count = row['Count']
                rating = row['Rating']

                netflix_collection_real.insert_one({
                    "MovieId": int(name),
                    "Rating": rating,
                    "Count": count,
                    "Sum": sum
                })
                print(f"Inserted Netflix Rating Pre-processed tv show: {name}")
            except Exception:
                continue