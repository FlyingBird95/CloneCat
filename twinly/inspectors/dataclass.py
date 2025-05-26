from dataclasses import is_dataclass

from twinly.attributes import Attribute
from twinly.inspectors.base import Inspector


class DataclassInspector(Inspector):
    """Inspector class for inspecting dataclasses."""

    def validate(self) -> None:
        if not is_dataclass(self.meta_class.model):
            raise ValueError(f"{self.meta_class.model} is not a dataclass.")

    @property
    def all_twinly_attributes(self) -> set[Attribute]:
        return set()

    @staticmethod
    def get_hash_key(obj_to_clone):
        return id(obj_to_clone)
