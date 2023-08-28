from utils import tv_shows_collection
import csv
import os

def insertTVShows():
    tv_shows_collection.drop()
    skip = 0
    inserted = 0
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.abspath(os.path.join(script_dir, '..', 'dataset'))
    csv_path = os.path.join(dataset_dir, 'tv_shows.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Insert each row into MongoDB
            try:
                name = row['Title']
                release_date = row['Year']
                ratings = {
                    "rotten_rating": row['Rotten Tomatoes'],
                    "imdb_rating": row['IMDb'],
                }
                platforms = []
                if row['Netflix'] == "1":
                    platforms.append("Netflix")
                if row['Prime Video'] == "1":
                    platforms.append("Prime Video")
                if row['Disney+'] == "1":
                    platforms.append("Disney+")

                tv_shows_collection.insert_one({
                    "title": name,
                    "release_date": release_date,
                    "ratings": ratings,
                    "platforms": platforms
                })
                print(f"Inserted tv show: {name}")
                inserted += 1
            except Exception:
                skip += 1
                continue

    print(f"Inserted {inserted} tv shows, but {skip} skipped ")