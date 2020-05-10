# Women-In-Movies

## Basic dataset from bechdeltest.com

The basic dataset comes from bechdeltest.com's API. There is a `getAllMovies` method returns an array of JSON objects which contains all information on bechdeltest.com's movies list. The data was downladed and saved as JSON file named `all.json`.

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

Then execute `main.py` to process with the raw data. 

1. Use themoviedb.org's API to get details of each movie in the bechdeltest's movie dataset. E.g. country and genres.
2. Store the data into MySQL database, aiming to use SQL to get needed results more effectively.

Before executing `main.py`, make sure to apply the **API key** from [https://www.themoviedb.org/documentation/api](https://www.themoviedb.org/documentation/api) and replace the `APIKEY` variable in `main.py` with personal API key, and then launch a MySQL server with the data table definition from `db.sql`.

## Data processing with Python

Execute three Python files separately to generate the data that used for drawing the charts.

-   `rating.py`
-   `country.py`
-   `genres.py`

Three JSON files will be generated in the `html` folder.

## Data visulization with JavaScript and HTML

Get access to the charts through `index.html`.
