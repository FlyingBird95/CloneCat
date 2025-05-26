from .utils import Entity


class CloneCatRegistry(dict):
    """Registry to add and retrieve entities.

    This registry is useful to retrieve newly created entities based on the old object.

    For example, a library has multiple books,
    and a book can be recommended by another book.
    In code, this looks as:
    book = Book()
    library = Library(books=[book, Book(recommended_by=book)])

    When cloning the library,
    the second newly created book should link to the first newly created book.
    This is possible using this registry.
    """

    def __setitem__(self, key: Entity, value: Entity) -> None:
        """Add the new entity to the registry.

        Raises an AssertionError if the new entity was already registered.
        """
        if key in self:
            raise ValueError(f"{key} is already registered")
        return super().__setitem__(key, value)
