import pymysql
import json

conn = pymysql.connect("127.0.0.1", "root", "", "film_data")


def get_bechdeltest_rating_stats_data():
    with conn:
        cur = conn.cursor()
        data = []
        for y in range(1930, 2020):
            cur.execute(
                "select year,count(*),rating from bechdeltest_all_movies where year=%s group by rating"
                % (y)
            )
            r = cur.fetchall()
            y = str(y)
            year_data = [
                {"year": y, "rating": "0", "value": 0},
                {"year": y, "rating": "1", "value": 0},
                {"year": y, "rating": "2", "value": 0},
                {"year": y, "rating": "3", "value": 0},
            ]
            for ir in r:
                for i in range(4):
                    if year_data[i]["rating"] == str(ir[2]):
                        year_data[i]["value"] = ir[1]
                        break
            for yd in year_data:
                data.append(yd)
        print(len(data))
        with open("./html/rating.json", "w") as f:
            json.dump(data, f)


if __name__ == "__main__":
    get_bechdeltest_rating_stats_data()
