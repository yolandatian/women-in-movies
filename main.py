import pymysql
import json
import requests

conn = pymysql.connect("127.0.0.1", "root", "", "film_data")

APIKEY = "e74f50eae5ea7218bc252b1d22a7722c"


# Get movie detail by TMDB(themoviedb.org) API
def get_detail_by_imdbid(imdb_id: str):
    # get tmdbID by imdbID
    r = requests.get(
        "https://api.themoviedb.org/3/find/%s" % imdb_id,
        params={"api_key": APIKEY, "language": "en-US", "external_source": "imdb_id"},
    )
    if r.status_code != 200:
        return None
    d = r.json()

    # get movie detail by tmdb ID
    tmdb_id = d["movie_results"][0]["id"]
    r = requests.get(
        "https://api.themoviedb.org/3/movie/%s" % tmdb_id,
        params={"api_key": APIKEY, "language": "en-US"},
    )
    if r.status_code != 200:
        return None
    d = r.json()
    d["imdb_id"] = imdb_id
    return d


# Import bechdeltest rating dataset to MySQL database
def bechdeltest_ratings_to_db():
    with open("./all.json") as f:
        data = json.load(f)
        with conn:
            cur = conn.cursor()
            for film in data:
                try:
                    cur.execute(
                        "INSERT INTO bechdeltest_all_movies(title, imdbid, rating, year) VALUES ('%s','%s','%s','%s')"
                        % (film["title"], film["imdbid"], film["rating"], film["year"])
                    )
                    conn.commit()
                except Exception as e:
                    print("error insert", e)


# Get more detail of each movie in bechdeltest's dataset
def bechdeltest_movie_detail_to_db():
    detail_data = []

    # get movie detail from TMDB API
    with open("./all.json") as f:
        data = json.load(f)
        i = 0
        for m in data:
            i += 1
            imdb_id = "tt" + m["imdbid"]
            movie = get_detail_by_imdbid(imdb_id)
            if movie is None:
                print("get detail error ", imdb_id)
            else:
                detail_data.append(movie)

    # import movie detail to local database
    with conn:
        cur = conn.cursor()
        for movie in detail_data:
            try:
                country = ""
                if len(movie["production_countries"]) != 0:
                    country = movie["production_countries"][0]["name"]
                vote_count = int(movie["vote_count"])
                vote_average = float(movie["vote_average"])
                query = """INSERT INTO tmdb_movie(imdb_id,tmdb_id, title,country, votes, user_rating) VALUES (%s,%s,%s,%s,%s,%s)"""
                cur.execute(
                    query=query,
                    args=(
                        movie["imdb_id"],
                        movie["id"],
                        movie["title"],
                        country,
                        vote_count,
                        vote_average,
                    ),
                )
                conn.commit()
            except Exception as e:
                print("error", e)


# Add rating data to `tmdb_movie` data table
def add_rating():
    with conn:
        cur = conn.cursor()
        cur.execute("select * from bechdeltest_all_movies")
        conn.commit()
        all_movie = cur.fetchall()
        for m in all_movie:
            imdb_id = "tt" + str(m[2])
            rating = m[3]
            year = m[4]
            cur.execute(
                "update tmdb_movie set `year`='%s',`rating`='%s' where `imdb_id`='%s'"
                % (year, rating, imdb_id)
            )
            conn.commit()


# Add movie's genres to `genres` data table
def add_genre_data():
    with open("./tmdb-movie.json") as f:
        data = json.load(f)
        with conn:
            cur = conn.cursor()
            for movie in data:
                for g in movie["genres"]:
                    try:
                        query = """INSERT INTO genres(imdb_id,genre) VALUES (%s,%s)"""
                        cur.execute(query=query, args=(movie["imdb_id"], g["name"]))
                        conn.commit()
                    except Exception as e:
                        print("error", e, g)


if __name__ == "__main__":
    bechdeltest_ratings_to_db()
    bechdeltest_movie_detail_to_db()
    add_rating()
    add_genre_data()
