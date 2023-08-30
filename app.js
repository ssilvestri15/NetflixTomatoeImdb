const express = require('express');
const app = express();
const port = 3000;
const db = require('./db/mongodb');

app.use(express.urlencoded({extended: true}));
app.use(express.static('public'));

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
    try {

        const newMovie = {
            name: req.body.name,
            info: req.body.info,
            genres: req.body.genres,
            directors: req.body.directors,
            authors: req.body.authors,
            release_date: req.body.release_date,
            runtime: req.body.runtime,
            production_company: req.body.production_company,
            ratings: {
                rotten_rating: req.body.rotten_rating,
                netflix_rating: req.body.netflix_rating,
                imdb_rating: req.body.imdb_rating
            }
        };
        await db.addItem(newMovie);
        res.redirect('/');
    } catch (error) {
        console.error('Errore durante l\'inserimento del film:', error);
        res.status(500).send('Si è verificato un errore durante l\'inserimento del film.');
    }
});

app.post('/updateItem', async (req, res) => {
    const itemId = req.body._id;
    try {
        const updatedData = {
            name: req.body.name,
            info: req.body.info,
            genres: req.body.genres,
            directors: req.body.directors,
            authors: req.body.authors,
            release_date: req.body.release_date,
            runtime: req.body.runtime,
            production_company: req.body.production_company,
            ratings: {
                rotten_rating: req.body.rotten_rating,
                netflix_rating: req.body.netflix_rating,
                imdb_rating: req.body.imdb_rating
            }
        };

        const result = await db.updateItem(itemId, updatedData)
        console.log(result)
        if (result.matchedCount === 0) {
            return res.status(404).json({ message: 'Elemento non trovato' });
        }

        res.json({ message: 'Elemento aggiornato con successo' });
    } catch (error) {
        console.error('Errore durante l\'aggiornamento:', error);
        res.status(500).json({ message: 'Errore durante l\'aggiornamento' });
    }
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