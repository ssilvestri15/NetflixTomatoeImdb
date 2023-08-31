const express = require('express');
const app = express();
const port = 3000;
const db = require('./db/mongodb');

app.use(express.urlencoded({extended: true}));
app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

app.get('/listaFilm', (req, res) => {
    res.sendFile(__dirname + '/public/listaFilm.html');
});

app.get('/insertFilm', (req, res) => {
    res.sendFile(__dirname + '/public/insertFilm.html');
});

app.get('/updateFilm', (req, res) => {
    res.sendFile(__dirname + '/public/updateFilm.html');
});

app.get('/items', async (req, res) => {
    try {
        const genres = req.query.genres;
        const release_date = req.query.release_date;
        const directors = req.query.directors;
        const type = req.query.type;
        const platform = req.query.platform;
        const rating_platform = req.query.rating_platform;
        const rating_platform_value = req.query.rating_platform_value;
        const filters = {
            genres: genres === undefined ? "" : genres,
            release_date:  release_date === undefined ? "" : release_date,
            directors:  directors === undefined ? "" : directors,
            type:  type === undefined ? "movie" : type,
            platform:  platform === undefined ? "" : platform,
            rating_platform:  rating_platform === undefined ? "" : rating_platform,
            rating_platform_value:  rating_platform_value === undefined ? "" : rating_platform_value
        };
        const items = await db.getItems(filters);
        res.json(items);
    } catch (error) {
        console.error('Errore durante il recupero dei film:', error);
        res.status(500).send('Si è verificato un errore durante il recupero dei film.');
    }
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
        res.redirect('/listaFilm');
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

        res.redirect('/listaFilm');
    } catch (error) {
        console.error('Errore durante l\'aggiornamento:', error);
        res.status(500).json({ message: 'Errore durante l\'aggiornamento' });
    }
});


app.post('/removeItem', async (req, res) => {
    const itemId = req.body.id
    try {
        const result = await db.removeItem(itemId);

        if (result.deletedCount === 1) {
            console.log('Cancellazione avvenuta con successo.');
            res.redirect('/listaFilm');
        } else {
            console.log('Nessun item corrispondente trovato per la cancellazione.');
        }
    } catch (error) {
        console.error('Si è verificato un errore durante la cancellazione:', error);
    }
});

//serie tv
app.get('/listaSerie', (req, res) => {
    res.sendFile(__dirname + '/public/listaSerie.html');
});

app.get('/insertSerie', (req, res) => {
    res.sendFile(__dirname + '/public/insertSerie.html');
});
app.get('/updateSerie', (req, res) => {
    res.sendFile(__dirname + '/public/updateSerie.html');
});

app.post('/addSerie', async (req, res) => {
    try {

        let selectedDate = new Date(req.body.release_date);
        let year = selectedDate.getFullYear();

        let rotten = `${req.body.rotten_rating}/100`
        let imdb = `${req.body.imdb_rating}/100`

        const newSerie = {
            title: req.body.title,
            release_date: year,
            ratings: {
                rotten_rating: rotten,
                imdb_rating: imdb
            },
            platforms: req.body.platforms
        };
        await db.addSerie(newSerie);
        res.redirect('/listaSerie');
    } catch (error) {
        console.error('Errore durante l\'inserimento della serie TV:', error);
        res.status(500).send('Si è verificato un errore durante l\'inserimento della serie TV.');
    }
});

app.post('/updateSerieTV', async (req, res) => {
    const itemId = req.body._id;

    let selectedDate = new Date(req.body.release_date);
    let year = selectedDate.getFullYear();

    let rotten = `${req.body.rotten_rating}/100`
    let imdb = `${req.body.imdb_rating}/100`

    try {
        const updatedSerie = {
            title: req.body.title,
            release_date: year,
            ratings: {
                rotten_rating: rotten,
                imdb_rating: imdb
            },
            platforms: req.body.platforms
        };

        const result = await db.updateSerie(itemId, updatedSerie)
        console.log(result)
        if (result.matchedCount === 0) {
            return res.status(404).json({ message: 'Elemento non trovato' });
        }

        res.redirect('/listaSerie');
    } catch (error) {
        console.error('Errore durante l\'aggiornamento:', error);
        res.status(500).json({ message: 'Errore durante l\'aggiornamento' });
    }
});


app.post('/removeSerie', async (req, res) => {
    const itemId = req.body.id
    try {
        const result = await db.removeSerie(itemId);

        if (result.deletedCount === 1) {
            console.log('Cancellazione avvenuta con successo.');
            res.redirect('/listaSerie');
        } else {
            console.log('Nessun item corrispondente trovato per la cancellazione.');
        }
    } catch (error) {
        console.error('Si è verificato un errore durante la cancellazione:', error);
    }
});


// Connect to MongoDB
db.connect().then(() => {
    app.listen(port, () => {
        console.log(`Server is running on port ${port}`);
    });
});