from netflix import getNetflixMovies, getNetflixRating, insertNetflixPreProcessed
from rotten import getRottenMovies
from imdb import getIMDBMovies
from tv_shows import insertTVShows
from utils import movies_collection, makeIntersection, netflix_collection_real

def main():

    pre_processed = True

    if pre_processed:
        insertNetflixPreProcessed()

    insertTVShows()

    rotten_movies_small, rotten_movies_ratings, rotten_movies_full = getRottenMovies()
    netflix_movies, netflix_ids = getNetflixMovies()
    imdb_movies, imdb_movies_full = getIMDBMovies()

    # Find the intersection of the two dictionaries
    movies_1 = makeIntersection(rotten_movies_small, netflix_movies)
    movies_2 = makeIntersection(movies_1, imdb_movies)

    movies_collection.drop()
    for key in movies_2:
        print(f"Adding movie: {key}")
        #insert movie into collection
        movies_collection.insert_one(rotten_movies_full[key].__dict__)
        print(f"Adding ratings to movie: {key} with id: {netflix_ids[key]}")

        netflix_rating = None
        if (pre_processed):
            netflix_rating = getNetflixRating(netflix_ids[key], key, True)
        else:
            netflix_collection_real.drop()
            netflix_rating = getNetflixRating(netflix_ids[key], key, False)
        
        if (netflix_rating is None):
            print(f"Skipping movie: {key}")
            continue

        ratings_data = {
            "rotten_rating": rotten_movies_ratings[key].num,
            "netflix_rating": netflix_rating.num,
            "imdb_rating": imdb_movies_full[key].num
        }
    
        #update element in collection
        filter_query = {"name": rotten_movies_full[key].name, "release_date": rotten_movies_full[key].release_date} 
        update_operation = {
            "$set": {"ratings": ratings_data}
        }
        movies_collection.update_one(filter = filter_query, update=update_operation)
    
    print(f"Found {len(movies_2)} movies in the intersection")

if __name__ == "__main__":
    main()