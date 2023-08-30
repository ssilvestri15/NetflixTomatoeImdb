
# POPCHIPS 🎬🍿

Welcome to the NetflixTomatoeImdb repository! Here, we're all about movies, data, and a touch of analytics. 🎉

## Table of Contents

- [Introduction](#introduction)
- [Datasets](#datasets)
- [Data Processing](#data-processing)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Features](#features)
- [License](#license)

## Introduction

Lights, camera, code! Our project revolves around building a web application that displays movie ratings and allows you to dive into some fascinating analytics. Whether you're a cinephile or just looking for your next movie night pick, this web app has got you covered! 😄🍕

## Datasets

We've curated a selection of datasets to power our movie magic:

- Rotten Tomatoes Dataset 🍅: [Rotten Tomatoes Movies and Critic Reviews Dataset](https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset)
- Netflix Dataset 🍿: [Netflix Movie Ratings Dataset](https://www.kaggle.com/datasets/evanschreiner/netflix-movie-ratings)
- IMDb Dataset 🎥: [IMDb Movie Reviews Dataset](https://ieee-dataport.org/open-access/imdb-movie-reviews-dataset)
- TV Shows Dataset: [TV Shows Dataset](https://www.kaggle.com/datasets/ruchi798/tv-shows-on-netflix-prime-video-hulu-and-disney)

## Data Processing

We've used some Python wizardry 🧙‍♂️ to clean and process our datasets, ensuring they're ready for the spotlight. Our Python script takes care of the data cleaning and transformation tasks, getting them all set to shine on the web app stage.

## Technologies Used

- Python 🐍
- Node.js 🟢
- Express.js 🚀
- MongoDB 🍃
- HTML/CSS/JavaScript 🌐

## Getting Started

Ready to embark on your movie adventure? Here's how to get started:

1. Clone this repository.
2. Install Node.js and MongoDB if you haven't already.
3. Run **`npm install`** to install project dependencies.
4. Run **`pip install -r requirements.txt`** to install project dependencies.
5. Start MongoDB.
6. Run **`py ./script/csv_to_mongo.py`** to populate the db.
7. Run **`npm start`** to launch the web app.
8. Open your favorite web browser and navigate to http://localhost:3000.

If you want to use the whole Netflix Review Dataset you need to do this:
1. All the steps above until 5.
2. Download the Netflix Dataset.
3. Manually import **`Netflix_User_Ratings.csv`** into MongoDB and call the collection **`netflix_ratings`** (it may take a long time).
4. Create an index for the collection **`netflix_ratings`** on the field **`MovieId`** (it may take a long time).
5. Edit the **`csv_to_mongo.py`** accordingly at your needings.
6. Run **`py ./script/csv_to_mongo.py`** to populate the db.
7. Run **`npm start`** to launch the web app.
8. Open your favorite web browser and navigate to http://localhost:3000.

## Features

Our web app is a movie lover's dream come true:

- Browse movie ratings from Rotten Tomatoes, Netflix, and IMDb.
- Enjoy insightful analytics and trends.
- Perform Create, Read, Update, and Delete (CRUD) operations on movie data.
- Have a laugh at some movie-related jokes we've sprinkled throughout the app. 😄🎉

## License

This project is licensed under the MIT License, so feel free to clone, modify, and distribute it as you please. Just remember to credit us for the cinematic magic! 🎥✨

Grab your popcorn and join us on this exciting coding journey! 🍿🎉🚀

## 

Made with ❤️ by Simone Silvestri, Matteo Ercolino and Carmine Pastore
