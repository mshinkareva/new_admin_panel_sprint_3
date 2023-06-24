from datetime import datetime
from time import sleep
from typing import Generator

from psycopg import connect, ServerCursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row

from settings import database_settings
from state.json_file_storage import JsonFileStorage
from state.models import Movie, State
from workers.ES_Worker import ESWorker
from workers.PG_Worker import PGWorker
from workers.decorators import coroutine
from workers.logger import logger
from workers.queries import FILM_WORKS_QUERY

STATE_KEY = 'last_movies_updated'


@coroutine
def fetch_changed_movies(
    cursor, next_node: Generator
) -> Generator[datetime, None, None]:
    while last_updated := (yield):
        logger.info('Fetching movies updated after %s', last_updated)
        cursor.execute(FILM_WORKS_QUERY, (last_updated,))
        while results := cursor.fetchmany(size=100):
            next_node.send((last_updated, results))


@coroutine
def transform_movies(next_node: Generator) -> Generator:
    pg_worker = PGWorker()
    last_updated = None
    while True:
        last_updated, movie_dicts = yield last_updated
        batch = []
        for movie_dict in movie_dicts:
            movie_dict['actors'] = pg_worker.get_actors(movie_dict['id'])
            movie_dict['directors'] = pg_worker.get_directors(movie_dict['id'])
            movie_dict['writers'] = pg_worker.get_writers(movie_dict['id'])
            movie_dict['genres'] = pg_worker.get_genres(movie_dict['id'])
            movie = transform(Movie(**movie_dict))
            logger.info(movie)
            batch.append(movie)
        next_node.send((last_updated, batch))


def transform(data):
    id = str(data.id)
    title = data.title
    description = data.description or ''
    imdb_rating = data.rating
    genre = [genre.name for genre in data.genres] if data.genres else ''
    director = (
        [director.name for director in data.directors][0] if data.directors else ''
    )
    actors_names = [actors_name.name for actors_name in data.actors]
    writers_names = [writers_name.name for writers_name in data.writers]
    actors = [{'id': str(actor.id), 'name': actor.name} for actor in data.actors]
    writers = [{'id': str(writer.id), 'name': writer.name} for writer in data.writers]
    return {
        'id': id,
        'title': title,
        'description': description,
        'imdb_rating': imdb_rating,
        'genre': genre,
        'director': director,
        'actors_names': actors_names,
        'writers_names': writers_names,
        'actors': actors,
        'writers': writers,
    }


@coroutine
def save_movies(state: State) -> Generator:
    es_worker = ESWorker()
    es_worker.create_index('movies', 'init_scripts/es_schema.json')
    last_updated = None
    while True:
        last_updated, movies = yield last_updated
        logger.info(f'Received for saving {len(movies)} movies')
        es_worker.load('movies', movies)
        state.set_state(STATE_KEY, str(last_updated))


def main():
    state = State(JsonFileStorage(logger=logger))
    dsn = make_conninfo(**database_settings.dict())

    with connect(dsn, row_factory=dict_row) as conn, ServerCursor(
        conn, 'fetcher'
    ) as cur:
        saver_coro = save_movies(state)
        transformer_coro = transform_movies(next_node=saver_coro)
        fetcher_coro = fetch_changed_movies(cur, transformer_coro)
        last_movies_updated = state.get_state(STATE_KEY) or str(datetime.min)

        while True:
            logger.info('Starting ETL process for updates ...')
            fetcher_coro.send(last_movies_updated)
            sleep(5)


if __name__ == '__main__':
    main()
