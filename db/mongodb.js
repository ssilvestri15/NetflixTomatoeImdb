const MongoClient = require('mongodb').MongoClient;
const ObjectId = require('mongodb').ObjectId;

const url = 'mongodb://localhost:27017';
const dbName = 'netflixtomatoes';
const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true });

let db;

async function connect() {
  await client.connect();
  db = client.db(dbName);
}

function getItems(filters) {

  console.log(filters);

  if (!filters) {
    return db.collection('movies').find().toArray();
  }

  if (filters.type === 'movie') {

    const filterQuery = {};

    if (filters.genres) {
      const genresRegex = new RegExp(`.*${filters.genres}.*`, 'i');
      filterQuery.genres = filters.genresRegex;
    }

    if (filters.release_date) {
      filterQuery.release_date = { $regex: `^${filters.release_date}-` };
    }

    if (filters.directors) {
      const directorsRegex = new RegExp(`.*${filters.directors}.*`, 'i');
      filterQuery.directors = { $regex: directorsRegex};
    }

    return db.collection('movies').find(filterQuery).toArray();

  } else {

    const filterQuery = {};

    if (filters.release_date) {
      filterQuery.release_date = filters.release_date;
    }

    if (filters.platform) {
      //check if is an array
      filterQuery.platforms = { $in: [filters.platform] };
    }

    if (filters.rating_platform && filters.rating_platform_value) {
      const platform = filters.rating_platform == 'rotten_tomatoes' ? 'rotten_rating' : 'imdb_rating';
      const value_to_search = filters.rating_platform == 'rotten_tomatoes' ? `${filters.rating_platform_value}/100` : `${filters.rating_platform_value}/10`;
      filterQuery[`ratings.${platform}`] = value_to_search;
    }

    console.log(filterQuery);
    return db.collection('tv_shows').find(filterQuery).toArray();
  }

}

function addItem(item) {
  return db.collection('movies').insertOne(item);
}

function updateItem(itemId, item) {
  return db.collection('movies').updateOne({ _id: new ObjectId(itemId) }, { $set: item });
}

function removeItem(itemId) {
  return db.collection('movies').deleteOne({ _id: itemId });
}



module.exports = {
  connect,
  getItems,
  addItem,
  removeItem,
  updateItem,
};
