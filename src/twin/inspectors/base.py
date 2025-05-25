from abc import ABC, abstractmethod
from typing import TypeVar

from ..attributes import Attribute
from ..twin import Twin

AttributeType = TypeVar("AttributeType", bound=Attribute)


class Inspector(ABC):
    """Inspector class to extract the Attribute from a class.

    This is an internal utility class, and not intended to be used outside this package.
    """

    def __init__(self, class_to_inspect: type[Twin]):
        self.meta_class = class_to_inspect.Meta

    @abstractmethod
    def validate(self) -> None:
        """Validate whether class attributes are defined properly."""

    @property
    @abstractmethod
    def all_twin_attributes(self) -> set[Attribute]:
        """Returns all twin attributes."""
