import pymysql
import json

conn = pymysql.connect("127.0.0.1", "root", "", "film_data")


def get_country_stat_data():
    data = []

    # 排序，加平均水平
    final_data = []
    with conn:
        cur = conn.cursor()
        # select country, count(*) as count from tmdb_movie where country<>'' group by country order by count desc limit 20
        countries = [
            "United States of America",
            "United Kingdom",
            "France",
            "Canada",
            "Japan",
            "Germany",
            "Spain",
            "Australia",
            "Italy",
            "India",
            "Belgium",
            "China",
            "Denmark",
            "Hong Kong",
            "Sweden",
            "Ireland",
            "South Korea",
            "Brazil",
            "Mexico",
            "New Zealand",
        ]

        for country in countries:
            single = [
                {"country": country, "rating": "3", "value": 0.0},
                {"country": country, "rating": "2", "value": 0.0},
                {"country": country, "rating": "1", "value": 0.0},
                {"country": country, "rating": "0", "value": 0.0},
            ]
            cur.execute(
                "select country,rating, count(*) from tmdb_movie where country = '%s' and rating in (0,1,2,3) group by rating;"
                % country
            )
            conn.commit()
            r = cur.fetchall()
            total = 0
            for ir in r:
                total += ir[2]
            print(country, total)
            for ir in r:
                for i in range(len(single)):
                    if single[i]["rating"] == str(ir[1]):
                        single[i]["value"] = float(ir[2] / total)
                        break
            data.append({"country": country, "data": single})
    # Add average data
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
                    "country": "All",
                    "rating": "3",
                    "value": total3 / (total0 + total1 + total2 + total3),
                },
                {
                    "country": "All",
                    "rating": "2",
                    "value": total2 / (total0 + total1 + total2 + total3),
                },
                {
                    "country": "All",
                    "rating": "1",
                    "value": total1 / (total0 + total1 + total2 + total3),
                },
                {
                    "country": "All",
                    "rating": "0",
                    "value": total0 / (total0 + total1 + total2 + total3),
                },
            ],
        }
    )

    # Top ranking with highest percentage of passed rating3
    def sort_country(elem):
        return elem["data"][0]["value"]

    data.sort(key=sort_country)
    for d in data:
        final_data.extend(d["data"])
    # Write final result into country.json that used to generate charts
    with open("./html/country.json", "w") as f:
        json.dump(final_data, f)


if __name__ == "__main__":
    get_country_stat_data()
