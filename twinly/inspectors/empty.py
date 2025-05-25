from ..attributes import Attribute
from .base import Inspector


class EmptyInspector(Inspector):
    """Empty inspector for when models shouldn't be inspected."""

    def validate(self) -> None:
        """Validate whether class attributes are defined properly."""

    @property
    def all_twinly_attributes(self) -> set[Attribute]:
        return set()
