from abc import ABC, abstractmethod
from typing import TypeVar

from ..attributes import Attribute
from ..clonecat import CloneCat

AttributeType = TypeVar("AttributeType", bound=Attribute)


class Inspector(ABC):
    """Inspector class to extract the Attribute from a class.

    This is an internal utility class, and not intended to be used outside this package.
    """

    def __init__(self, class_to_inspect: type[CloneCat]):
        self.meta_class = class_to_inspect.Meta

    @abstractmethod
    def validate(self) -> None:
        """Validate whether class attributes are defined properly."""

    @property
    @abstractmethod
    def all_clone_cat_attributes(self) -> set[Attribute]:
        """Returns all CloneCat attributes."""

    @staticmethod
    def get_hash_key(obj_to_clone: object) -> object:
        """Given the instance to clone, return the hash of the instance.

        When an object is not hashable,
        this method can be overridden to return a unique hash key for an instance.
        """
        return obj_to_clone
