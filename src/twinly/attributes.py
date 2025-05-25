from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Optional, Union

from .import_helper import import_copy_cat_class
from .registry import TwinlyRegistry
from .twinly import Twinly
from .utils import NOT_SET, Entity


class Attribute(Generic[Entity], ABC):
    """Base attribute class."""

    def __init__(self) -> None:
        self.name: str = NOT_SET

    def __set_name__(self, owner, name) -> None:
        """This method is automatically called when an attribute is created

        Usage:

        new_attribute = Attribute()

        This triggers __set_name__ with `name="new_attribute"`.
        ."""
        self.name = name

    @abstractmethod
    def get_value(self, obj_to_copy: Entity, registry: TwinlyRegistry):
        """Get the value"""


class Copy(Attribute):
    """Use this class to copy the attribute from the old instance.

    An example usage would be for Book.title;
    when copying a book, it should have the same author.
    Therefore, book.title must be defined as:
        Book.title = Copy()
    """

    def get_value(self, obj_to_copy: Entity, registry: TwinlyRegistry) -> Any:
        return getattr(obj_to_copy, self.name)


class Clone(Attribute):
    """Use this class to duplicate another attribute.

    An example is when cloning a Book, then Book.author should be duplicated as well.
    This can be defined as:
        author = Clone(CopyAuthor)

    There are three usages:

    1. Use as a decorator:
        @Clone()
        def author(self, registry: TwinlyRegistry):
            ...
    2. Use as a class attribute using typing:
        author = Clone(CopyAuthor)
    3. Use an instance of a CopyClass:
        author = Clone(Optional(CopyAuthor))
    """

    def __init__(self, inner_class: Union[type[Twinly], Optional[Twinly], str] = None):
        super().__init__()
        self._inner_class = inner_class
        self.getter_function = None

    @property
    def inner_class(self):
        if isinstance(self._inner_class, str):
            return import_copy_cat_class(self._inner_class)
        return self._inner_class

    def get_value(self, obj_to_copy, registry: TwinlyRegistry) -> None:
        if self.inner_class is not None:
            obj_to_clone = getattr(obj_to_copy, self.name)
            return self.inner_class.clone(obj_to_clone, registry)
        return self.getter_function(obj_to_copy, registry)

    def __call__(self, getter_function: Callable):
        self.getter_function = getter_function
        return self


class Ignore(Attribute):
    """Use this class if you don't want to copy the attribute of the old object."""

    def get_value(self, obj_to_copy: Entity, registry: TwinlyRegistry):
        return NOT_SET
