

FILM_WORKS_QUERY = 'SELECT "film_work"."id", "film_work"."title", "film_work"."description", ' \
                   '"film_work"."created_at", "film_work"."updated_at", "film_work"."rating", ' \
                   '"film_work"."type" FROM "content"."film_work" WHERE updated_at > %s ' \
                   'ORDER BY "film_work"."title" ASC'


ACTORS_QUERY = """
SELECT
    "person"."id",
    "person"."full_name" as "name"
FROM
    "content"."person_film_work"
JOIN
    "content"."person" ON "person_film_work"."person_id" = "person"."id"
WHERE
    "person_film_work"."film_work_id" = %(film_id)s
    AND "person_film_work"."role" = 'actor'
"""

DIRECTORS_QUERY = """
SELECT
    "person"."id",
    "person"."full_name" as "name"
FROM
    "content"."person_film_work"
JOIN
    "content"."person" ON "person_film_work"."person_id" = "person"."id"
WHERE
    "person_film_work"."film_work_id" = %(film_id)s
    AND "person_film_work"."role" = 'director'
    """

WRITERS_QUERY = """
SELECT
    "person"."id",
    "person"."full_name" as "name"
FROM
    "content"."person_film_work"
JOIN
    "content"."person" ON "person_film_work"."person_id" = "person"."id"
WHERE
    "person_film_work"."film_work_id" = %(film_id)s
    AND "person_film_work"."role" = 'writer'
"""

GENRES_QUERY = """
SELECT
    "genre"."id",
    "genre"."name"
FROM
    "content"."genre_film_work"
JOIN
    "content"."genre" ON "genre_film_work"."genre_id" = "genre"."id"
WHERE
    "genre_film_work"."film_work_id" = %(film_id)s
"""

MOVIE_DATA_QUERY = """
SELECT
    'actor' as role_type,
    "person"."id",
    "person"."full_name" as "name"
FROM
    "content"."person_film_work"
JOIN
    "content"."person" ON "person_film_work"."person_id" = "person"."id"
WHERE
    "person_film_work"."film_work_id" = %(film_id)s
    AND "person_film_work"."role" = 'actor'

UNION

SELECT
    'director' as role_type,
    "person"."id",
    "person"."full_name" as "name"
FROM
    "content"."person_film_work"
JOIN
    "content"."person" ON "person_film_work"."person_id" = "person"."id"
WHERE
    "person_film_work"."film_work_id" = %(film_id)s
    AND "person_film_work"."role" = 'director'

UNION

SELECT
    'writer' as role_type,
    "person"."id",
    "person"."full_name" as "name"
FROM
    "content"."person_film_work"
JOIN
    "content"."person" ON "person_film_work"."person_id" = "person"."id"
WHERE
    "person_film_work"."film_work_id" = %(film_id)s
    AND "person_film_work"."role" = 'writer'

UNION

SELECT
    'genre' as role_type,
    "genre"."id",
    "genre"."name" as "name"
FROM
    "content"."genre_film_work"
JOIN
    "content"."genre" ON "genre_film_work"."genre_id" = "genre"."id"
WHERE
    "genre_film_work"."film_work_id" = %(film_id)s

"""