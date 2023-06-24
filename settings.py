from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...

    class Config:
        env_prefix = 'postgres_'
        env_file = (
            '/Users/mariya.shinkareva/PycharmProjects/new_admin_panel_sprint_3/.env'
        )
        env_file_encoding = 'utf-8'


class ElasticSearchSettings(BaseSettings):
    host: str = ...
    port: int = ...

    class Config:
        env_prefix = 'es_'
        env_file = (
            '/Users/mariya.shinkareva/PycharmProjects/new_admin_panel_sprint_3/.env'
        )
        env_file_encoding = 'utf-8'

    def __str__(self):
        return f'http://{self.host}:{self.port}'


database_settings = DatabaseSettings()
es_settings = ElasticSearchSettings()
