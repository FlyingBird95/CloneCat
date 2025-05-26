import dataclasses
from datetime import datetime


@dataclasses.dataclass
class Author:
    first_name: str
    last_name: str


@dataclasses.dataclass
class Book:
    id: int
    author: Author
    title: str
    release_data: datetime
