# women-in-movies

## Basic dataset from bechdeltest.com

The basic dataset is from bechdeltest.com's API. There is a `getAllMovies` method returns an array of JSON objects which contains all information on all movies bechdeltest.com's movies list. We download that data and save as JSON file named `all.json`.

```json
[
    {
        "id": 8040,
        "rating": 0,
        "title": "Roundhay Garden Scene",
        "imdbid": "0392728",
        "year": 1888
    },
    //...
]
```

## Install Python dependencies

```
pip install -r requirements
```

## Get more data and import to MySQL

Then execute `main.py` to process with the raw data. It mainly does two things.

1. Use themoviedb.org's API to get details of each movie in the bechdeltest's movie dataset, like country and genres.
2. Store the data into MySQL database, so that we can use SQL to query the data and get results we want more effectively.

Before executing `main.py`, make sure you have already applied the **API key** from [https://www.themoviedb.org/documentation/api](https://www.themoviedb.org/documentation/api) and replaced the `APIKEY` variable in `main.py` with your own API key. And launch a MySQL server with the data table definition from `db.sql`.

## Data processing with Python

Execute three Python files above separately to generate the data for drawing the charts.

-   `rating.py`
-   `country.py`
-   `genres.py`

Three JSON files will be generated in the `html` folder.

## Data visulization with JavaScripy and HTML

Open the `index.html` to view the charts.
