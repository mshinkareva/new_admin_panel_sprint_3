import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Any
from typing import Union

from django.core.files.uploadedfile import UploadedFile
from pydantic import BaseModel
from .base_storage import BaseStorage

class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        try:
            state = self.storage.retrieve_state()
        except FileNotFoundError:
            state = dict()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        return self.storage.retrieve_state().get(key)


class PersonRole(BaseModel):
    id: uuid.UUID
    name: str


class Genre(BaseModel):
    id: uuid.UUID
    name: str


class Movie(BaseModel):
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


