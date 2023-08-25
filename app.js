const express = require('express');
const app = express();
const port = 3000;
const db = require('./db/mongodb');

app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

let items = [
  { id: 1, name: 'Item 1' },
  { id: 2, name: 'Item 2' },
  { id: 3, name: 'Item 3' },
];

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

app.get('/insertFilm', (req, res) => {
    res.sendFile(__dirname + '/public/insertFilm.html');
});

app.get('/items', async (req, res) => {
    const items = await db.getItems();
    res.json(items);
  });

app.post('/addItem', async (req, res) => {
    const newMovie = {
        name: req.body.name,
        info: req.body.info,
        genres: req.body.genres,
        directors: req.body.directors,
        authors: req.body.authors,
        release_date: req.body.release_date,
        runtime: req.body.runtime,
        production_company: req.body.production_company,
        rotten_rating: req.body.rotten_rating,
        netflix_rating: req.body.netflix_rating,
        imdb_rating: req.body.imdb_rating,
    };

    await db.addItem(newMovie);
    res.redirect('/');
});
  
  app.post('/removeItem', async (req, res) => {
    const itemId = require('mongodb').ObjectID(req.body.id);
    await db.removeItem(itemId);
    res.redirect('/');
  });

// Connect to MongoDB
db.connect().then(() => {
    app.listen(port, () => {
      console.log(`Server is running on port ${port}`);
    });
});