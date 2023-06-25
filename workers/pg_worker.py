import backoff
from psycopg import connect, ServerCursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row

from settings import database_settings
from state.models import Movie
from workers.queries import (
    FILM_WORKS_QUERY,
    WRITERS_QUERY,
    DIRECTORS_QUERY,
    ACTORS_QUERY,
    GENRES_QUERY, MOVIE_DATA_QUERY,
)


class PGWorker:
    pass

    def __init__(self):
        self.dsn = make_conninfo(**database_settings.dict())

    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def get_actors(self, film_id):
        with connect(self.dsn, row_factory=dict_row) as conn, ServerCursor(
            conn, 'fetcher'
        ) as cur:
            cur.execute(ACTORS_QUERY, {'film_id': film_id})
            return cur.fetchall()

    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def get_directors(self, film_id):
        with connect(self.dsn, row_factory=dict_row) as conn, ServerCursor(
            conn, 'fetcher'
        ) as cur:
            cur.execute(DIRECTORS_QUERY, {'film_id': film_id})
            return cur.fetchall()

    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def get_writers(self, film_id):
        with connect(self.dsn, row_factory=dict_row) as conn, ServerCursor(
            conn, 'fetcher'
        ) as cur:
            cur.execute(WRITERS_QUERY, {'film_id': film_id})
            return cur.fetchall()

    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def get_genres(self, film_id):
        with connect(self.dsn, row_factory=dict_row) as conn, ServerCursor(
            conn, 'fetcher'
        ) as cur:
            cur.execute(GENRES_QUERY, {'film_id': film_id})
            return cur.fetchall()

    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def get_movie_data(self, film_id):
        with connect(self.dsn, row_factory=dict_row) as conn, ServerCursor(
            conn, 'fetcher'
        ) as cur:
            cur.execute(MOVIE_DATA_QUERY, {'film_id': film_id})
            return cur.fetchall()

    @backoff.on_exception(backoff.expo, Exception, max_time=60)
    def extract(self):
        batch_size: int = 20
        with connect(self.dsn, row_factory=dict_row) as conn, ServerCursor(
            conn, 'fetcher'
        ) as cur:
            cur.execute(FILM_WORKS_QUERY)
            while True:
                films = cur.fetchmany(batch_size)
                if not films:
                    break
                for film in films:
                    film['actors'] = self.get_actors(film['id'])
                    film['directors'] = self.get_directors(film['id'])
                    film['writers'] = self.get_writers(film['id'])
                    film['genres'] = self.get_genres(film['id'])
                yield [Movie(**row) for row in films]
