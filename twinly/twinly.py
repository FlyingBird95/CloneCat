from abc import ABC, abstractmethod
from typing import Any, Generic, Type

from .registry import TwinlyRegistry
from .utils import NOT_SET, Entity


class Twinly(Generic[Entity], ABC):
    """Base class for copying SQLAlchemy models.

    This class is not supposed to be instantiated directly.
    Instead, create subclasses for specific entities.

    Usage:

    class CopyFoo(TwinLy):
        class Meta:
            model = Foo
            ignore = {Foo.first_attribute}
            copy = {Foo.second_attribute}

        third_attribute = Clone(TwinlyClassForThirdAttribute)
    """

    inspector_class = None

    @abstractmethod
    class Meta:
        """Define the model that should be instantiated below."""

        model: Type[Entity] = NOT_SET  # type: ignore
        ignore: set[Any] = set()
        copy: set[Any] = set()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.inspector_class is None:
            raise ValueError("Missing class attribute inspector_class.")

        if cls.Meta.model is NOT_SET:
            return  # class is an abstract class, so skip validation

        cls.inspector = cls.inspector_class(cls)

        if not hasattr(cls.Meta, "model") or cls.Meta.model is NOT_SET:
            raise ValueError(
                "Please specify an inner Meta class with 'model' attribute."
            )

        cls.inspector.validate()

    @classmethod
    def validate(cls, obj_to_copy: Entity) -> None:
        if not cls.is_correct_type(obj_to_copy):
            raise ValueError(
                f"Expected instance of {cls.Meta.model}, got {obj_to_copy.__class__}"
            )

    @classmethod
    def is_correct_type(cls, obj_to_copy: Entity) -> bool:
        return isinstance(obj_to_copy, cls.Meta.model)

    @classmethod
    def clone(cls, obj_to_copy: Entity, registry: TwinlyRegistry) -> Entity:
        """Copies the instance."""
        cls.validate(obj_to_copy)

        if obj_to_copy in registry:
            return registry[obj_to_copy]

        new_obj = cls.Meta.model()
        registry[obj_to_copy] = new_obj

        # Copy attributes
        for attr in cls.inspector.all_twinly_attributes:
            new_value = attr.get_value(obj_to_copy, registry)
            if new_value is not NOT_SET:
                setattr(new_obj, attr.name, new_value)

        # Trigger post-generation function if exists.
        if hasattr(cls, "__post_init__"):
            cls.__post_init__(new_obj)

        return new_obj
