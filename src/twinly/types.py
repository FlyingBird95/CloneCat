import typing

from .import_helper import import_copy_cat_class
from .inspectors.empty import EmptyInspector
from .registry import TwinlyRegistry
from .twinly import Twinly
from .utils import Entity


class Optional(Twinly):
    """Class for cloning optional instances.

    When the instance is None, then Optional.clone(...) returns None.
    When the instance is already copied, then it is not copied again,
    but the already copied instance is returned from the registry.

    Usage:
    1. Use directly:
        some_attribute = Clone(Optional(SomeTwinlyClass))
    2. When imports cannot be done directly, a creator function may also be passed:
        def get_some_twinly_class():
             return SomeTwinlyClass
        some_attribute = Clone(Optional(get_some_twinly_class))
    3. With a string location to a class (useful for solving circular imports):
        some_attribute = Clone(Optional("your_package.SomeTwinlyClass"))
    """

    inspector_class = EmptyInspector

    class Meta:
        model = None

    def __init__(self, inner_class: typing.Union[type[Twinly], Twinly, str]):
        self._inner_class = inner_class

    @property
    def inner_class(self):
        if isinstance(self._inner_class, str):
            return import_copy_cat_class(self._inner_class)

        return self._inner_class

    def validate(self, obj_to_copy: typing.Optional[Twinly]) -> None:
        if not self.is_correct_type(obj_to_copy):
            raise ValueError(
                f"Expected instance to be None or of type {obj_to_copy.__class__}, "
                f"got {obj_to_copy.__class__}"
            )

    def is_correct_type(self, obj_to_copy: Entity) -> bool:
        return obj_to_copy is None or self.inner_class.is_correct_type(obj_to_copy)

    def clone(
        self, obj_to_copy: typing.Optional[Entity], registry: TwinlyRegistry
    ) -> typing.Optional[Entity]:
        self.validate(obj_to_copy)
        if obj_to_copy is None:
            return None

        return self.inner_class.clone(obj_to_copy, registry)


class List(Twinly):
    """Class for cloning a list of instances.

    When an instance in the list is already copied,
    then it is not copied again, but the already copied instance is returned.

    Usage:
    1. Use directly with a class:
        some_attribute = Clone(List(SomeTwinlyClass))
    2. Use directly with an instance:
        some_attribute = Clone(List(Optional(SomeTwinlyClass)))
    3. With a string location to a class (useful for solving circular imports):
        some_attribute = Clone(List("your_package.SomeTwinlyClass"))
    """

    inspector_class = EmptyInspector

    class Meta:
        model = list

    def __init__(self, inner_class: typing.Union[Twinly, type[Twinly], str]):
        self._inner_class = inner_class

    @property
    def inner_class(self):
        if isinstance(self._inner_class, str):
            return import_copy_cat_class(self._inner_class)
        return self._inner_class

    def clone(
        self, obj_to_copy: list[Entity], registry: TwinlyRegistry
    ) -> list[Entity]:
        self.validate(obj_to_copy)
        return [self.inner_class.clone(obj, registry) for obj in obj_to_copy]


class Set(Twinly):
    """Class for cloning a set of instances.

    When an instance in the set is already copied,
    then it is not copied again, but the already copied instance is returned.

    Usage:
    1. Use directly with a class:
        some_attribute = Clone(Set(SomeTwinlyClass))
    2. Use directly with an instance:
        some_attribute = Clone(Set(Optional(SomeTwinlyClass)))
    3. With a string location to a class (useful for solving circular imports):
        some_attribute = Clone(Set("your_package.SomeTwinlyClass"))
    """

    inspector_class = EmptyInspector

    class Meta:
        model = set

    def __init__(self, inner_class: typing.Union[Twinly, type[Twinly], str]):
        self._inner_class = inner_class

    @property
    def inner_class(self):
        if isinstance(self._inner_class, str):
            return import_copy_cat_class(self._inner_class)
        return self._inner_class

    def clone(self, obj_to_copy: set[Entity], registry: TwinlyRegistry) -> set[Entity]:
        self.validate(obj_to_copy)
        return {self.inner_class.clone(obj, registry) for obj in obj_to_copy}


class OneOf(Twinly):
    """Class for cloning union types.

    An instance to be copied must be an instance of the classes
    defined in the arguments of this class.

    Usages:
    1. Use directly with a class:
        books = Clone(List(OneOf(BookA, BookB)))
    2. With a string location to a class (useful for solving circular imports):
        some_attribute = Clone(OneOf("your_package.BookA", "your_package.BookB"))
    """

    inspector_class = EmptyInspector

    class Meta:
        model = None

    def __init__(self, *inner_classes: typing.Union[type[Twinly], str]):
        super().__init__()
        self._inner_classes = inner_classes

    @property
    def inner_classes(self):
        classes = []
        for inner_class in self._inner_classes:
            if isinstance(inner_class, str):
                classes.append(import_copy_cat_class(inner_class))
            else:
                classes.append(inner_class)
        return classes

    def is_correct_type(self, obj_to_copy: Entity) -> bool:
        return any(
            inner_class.is_correct_type(obj_to_copy)
            for inner_class in self.inner_classes
        )

    def validate(self, obj_to_copy: Entity) -> None:
        if not self.is_correct_type(obj_to_copy):
            inner_classes = ",".join(
                str(inner_class) for inner_class in self.inner_classes
            )
            raise ValueError(
                f"Expected instance to be one of: {inner_classes}, "
                f"got {type(obj_to_copy)}"
            )

    def clone(self, obj_to_copy: Entity, registry: TwinlyRegistry) -> Entity:
        self.validate(obj_to_copy)

        try:
            inner_class = next(
                inner_class
                for inner_class in self.inner_classes
                if inner_class.is_correct_type(obj_to_copy)
            )
        except StopIteration:
            raise Exception(f"No class found for {obj_to_copy.__class__}")

        return inner_class.clone(obj_to_copy, registry)
