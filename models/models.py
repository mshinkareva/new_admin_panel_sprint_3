import uuid
from datetime import datetime
from typing import List, Optional
from typing import Union

from pydantic import BaseModel


class PersonRole(BaseModel):
    id: uuid.UUID
    name: str


class Genre(BaseModel):
    id: uuid.UUID
    name: str


class FilmWorkModelPyd(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    creation_date: Optional[Union[datetime, str]]
    file_path: Optional[str]
    rating: Optional[float]
    type: str
    created_at: Union[datetime, str]
    updated_at: Union[datetime, str]
    actors: Optional[List[PersonRole]]
    directors: Optional[List[PersonRole]]
    writers: Optional[List[PersonRole]]
    genres: Optional[List[Genre]]
