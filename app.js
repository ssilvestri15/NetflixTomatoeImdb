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

app.get('/items', async (req, res) => {
    const items = await db.getItems();
    res.json(items);
  });

  app.post('/addItem', async (req, res) => {
    const newItem = { name: req.body.name };
    await db.addItem(newItem);
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