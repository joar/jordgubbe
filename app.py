import asyncio
from typing import List, Optional, Generator, AsyncGenerator, AsyncIterable

import datetime as dt
import strawberry


@strawberry.type
class Actor:
    name: str
    birth_year: int

    @strawberry.field
    async def starred_in(self, info) -> AsyncIterable["Movie"]:
        for movie in MOVIES:
            if self.name in [actor.name for actor in movie.actors]:
                yield movie


@strawberry.type
class Movie:
    title: str
    release_year: int
    actors: List[Actor]


MOVIES = [
    Movie(
        title="A",
        release_year=dt.datetime.now(),
        actors=[Actor(name="A. Foo", birth_year=1)],
    ),
    Movie(
        title="B",
        release_year=dt.datetime.now(),
        actors=[Actor(name="A. Foo", birth_year=1)],
    ),
]

ACTORS = [actor for movie in MOVIES for actor in movie.actors]


@strawberry.type
class Query:
    @strawberry.field
    def movies(self, info) -> List[Movie]:
        return MOVIES

    @strawberry.field
    def get_actor_by_name(self, info, name: str) -> Optional[Actor]:
        for actor in ACTORS:
            if actor.name == name:
                return actor
        return None


@strawberry.type
class Event:
    number: int


@strawberry.type
class Subscription:
    @strawberry.field(is_subscription=True)
    async def count_up(self, info) -> Event:
        counter = 0
        while True:
            await asyncio.sleep(1)
            counter += 1
            yield Event(number=counter)


schema = strawberry.Schema(query=Query, subscription=Subscription)
