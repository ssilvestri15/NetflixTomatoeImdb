from utils import Movie, MovieInfo
import csv
import os

def getIMDBMovies():
    imdb_movies = {}
    imdb_movies_full = {}
    skip = 0
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.abspath(os.path.join(script_dir, '..', 'dataset'))
    csv_path = os.path.join(dataset_dir, 'imdb_movies.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Insert each row into MongoDB
            name = row['name']
            release_date = row['year']
            rating = row.get('rating')

            if (release_date is None or release_date == "" or rating is None):
                skip += 1
                continue

            try:
                rating = float(rating)
            except Exception:
                skip += 1
                continue

            key = f"{name.lower()}_{release_date.lower()}"
            imdb_movies[key] = Movie.create(name.lower(), release_date.lower())
            imdb_movies_full[key] = MovieInfo(key, float(rating))

    print(f"Found {len(imdb_movies_full)} imdb movies, but {skip} skipped ")
    return imdb_movies, imdb_movies_full