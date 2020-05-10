import pymysql
import json

conn = pymysql.connect("127.0.0.1", "root", "", "film_data")


# There are 19 genres among 8000+ movies from bechdeltest's dataset
# select genre, count(*) as count from genres group by genre order by count desc limit 20;
#
# Drama,4304
# Comedy,2935
# Thriller,1753
# Romance,1593
# Action,1389
# Adventure,1105
# Horror,1058
# Crime,949
# Science Fiction,894
# Fantasy,780
# Family,748
# Mystery,658
# Animation,551
# Music,350
# History,324
# War,243
# TV Movie,138
# Western,125
# Documentary,101
def get_genre_stats_data():
    genres = [
        "Drama",
        "Comedy",
        "Thriller",
        "Romance",
        "Action",
        "Adventure",
        "Horror",
        "Crime",
        "Science Fiction",
        "Fantasy",
        "Family",
        "Mystery",
        "Animation",
        "Music",
        "History",
        "War",
        "TV Movie",
        "Western",
        "Documentary",
    ]
    data = []
    final_data = []
    with conn:
        cur = conn.cursor()
        for genre in genres:
            cur.execute(
                """
            select count(*), rating
            from tmdb_movie
            where imdb_id in (select imdb_id from genres where genres.genre = '%s')
            and rating in (0, 1, 2, 3)
            group by rating
            order by rating
            """
                % genre
            )
            conn.commit()
            r = cur.fetchall()
            total = 0
            for ir in r:
                total += ir[0]
            single = [
                {"genre": genre, "rating": "3", "value": 0.0},
                {"genre": genre, "rating": "2", "value": 0.0},
                {"genre": genre, "rating": "1", "value": 0.0},
                {"genre": genre, "rating": "0", "value": 0.0},
            ]
            for ir in r:
                for i in range(len(single)):
                    if single[i]["rating"] == str(ir[1]):
                        single[i]["value"] = float(ir[0] / total)
                        break
            data.append({"genre": genre, "data": single})

    # 计算总体水平并加入数据列表
    total0 = 0
    total1 = 0
    total2 = 0
    total3 = 0
    for d in data:
        total3 += d["data"][0]["value"]
        total2 += d["data"][1]["value"]
        total1 += d["data"][2]["value"]
        total0 += d["data"][3]["value"]
    data.append(
        {
            "country": "All",
            "data": [
                {
                    "genre": "All",
                    "rating": "3",
                    "value": total3 / (total0 + total1 + total2 + total3),
                },
                {
                    "genre": "All",
                    "rating": "2",
                    "value": total2 / (total0 + total1 + total2 + total3),
                },
                {
                    "genre": "All",
                    "rating": "1",
                    "value": total1 / (total0 + total1 + total2 + total3),
                },
                {
                    "genre": "All",
                    "rating": "0",
                    "value": total0 / (total0 + total1 + total2 + total3),
                },
            ],
        }
    )

    # 为数据排序，rating3（通过测试）比例越高约靠前
    def sort_genre(elem):
        return elem["data"][0]["value"]

    data.sort(key=sort_genre)
    for d in data:
        final_data.extend(d["data"])
    # 最终结果写入genre.json文件，绘制图表所使用的为该json数据
    with open("./html/genre.json", "w") as f:
        json.dump(final_data, f)


if __name__ == "__main__":
    get_genre_stats_data()
