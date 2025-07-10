from dataclasses import dataclass, field
from itertools import batched
from typing import Generator, Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int = 3):
        self.per_page = per_page

    def __iter__(self) -> Generator[SomeRemoteData]:
        page = 1
        while True:
            query = Query(per_page=self.per_page, page=page)
            response = request(query)
            yield from response.results
            if response.next is None:
                break
            page = response.next


class Fibo:

    def __init__(self, n: int):
        self.now = 0
        self.next = 1
        self.count = 0
        self.end = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.end:
            raise StopIteration
        result = self.now
        self.now, self.next = self.next, self.now + self.next
        self.count += 1
        return result
