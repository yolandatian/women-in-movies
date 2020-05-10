CREATE SCHEMA IF NOT EXISTS `film_data` COLLATE `utf8mb4_general_ci`;

CREATE TABLE IF NOT EXISTS `bechdeltest_all_movies`
(
    `id`     INT AUTO_INCREMENT
        PRIMARY KEY,
    `title`  VARCHAR(255) NULL,
    `imdbid` VARCHAR(255) NULL,
    `rating` INT          NULL,
    `year`   INT          NULL,
    CONSTRAINT `bechdeltest_all_movies_imdbid_uindex`
        UNIQUE (`imdbid`)
);

CREATE TABLE IF NOT EXISTS `tmdb_movie`
(
    `imdb_id`     VARCHAR(255) NULL,
    `tmdb_id`     INT          NULL,
    `title`       VARCHAR(255) NULL,
    `votes`       INT          NULL,
    `user_rating` FLOAT        NULL,
    `country`     VARCHAR(255) NULL,
    `rating`      INT          NULL,
    `year`        INT          NULL,
    CONSTRAINT `imdb_movie_imdb_id_uindex`
        UNIQUE (`imdb_id`)
);

CREATE TABLE IF NOT EXISTS `genres`
(
    `imdb_id` VARCHAR(255) NULL,
    `genre`   VARCHAR(255) NULL
);