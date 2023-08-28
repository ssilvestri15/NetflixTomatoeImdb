from utils import Movie, MovieInfo, extract_year_from_date
import csv
import os

def getRottenMovies():
    rotten_movies_small = {}
    rotten_movies_ratings = {}
    rotten_movies_full = {}
    skip = 0
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.abspath(os.path.join(script_dir, '..', 'dataset'))
    csv_path = os.path.join(dataset_dir, 'rotten_tomatoes_movies.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
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
                skip += 1
            else:
                key = f"{name.lower()}_{date.lower()}"
                rating = row['audience_rating']

                if rating is None or rating == "" or not rating.isnumeric():
                    skip += 1
                    continue
            
                if key in rotten_movies_ratings:
                    skip += 1
                    continue
                else:
                    rotten_movies_full[key] = movie
                    rotten_movies_small[key] = Movie.create(name.lower(), date.lower())
                    rotten_movies_ratings[key] = MovieInfo(key, rating)

    print(f"Found {len(rotten_movies_full)} rotten movies, but {skip} skipped")
    return rotten_movies_small, rotten_movies_ratings, rotten_movies_full