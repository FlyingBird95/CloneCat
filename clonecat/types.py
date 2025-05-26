import typing

from .clonecat import CloneCat
from .import_helper import import_clone_cat_class
from .inspectors.empty import EmptyInspector
from .registry import CloneCatRegistry
from .utils import Entity


class Optional(CloneCat):
    """Class for cloning optional instances.

    When the instance is None, then Optional.clone(...) returns None.
    When the instance is already copied, then it is not copied again,
    but the already copied instance is returned from the registry.

    Usage:
    1. Use directly:
        some_attribute = Clone(Optional(SomeCloneCatClass))
    2. When imports cannot be done directly, a creator function may also be passed:
        def get_some_clone_cat_class():
             return SomeCloneCatClass
        some_attribute = Clone(Optional(get_some_clone_cat_class))
    3. With a string location to a class (useful for solving circular imports):
        some_attribute = Clone(Optional("your_package.SomeCloneCatClass"))
    """

    inspector_class = EmptyInspector

    class Meta:
        model = None

    def __init__(self, inner_class: typing.Union[type[CloneCat], CloneCat, str]):
        self._inner_class = inner_class

    @property
    def inner_class(self):
        if isinstance(self._inner_class, str):
            return import_clone_cat_class(self._inner_class)

        return self._inner_class

    def validate(self, obj: typing.Optional[CloneCat]) -> None:
        if not self.is_correct_type(obj):
            raise ValueError(
                f"Expected instance to be None or of type {obj.__class__}, "
                f"got {obj.__class__}"
            )

    def is_correct_type(self, obj: Entity) -> bool:
        return obj is None or self.inner_class.is_correct_type(obj)

    def clone(
        self, obj: typing.Optional[Entity], registry: CloneCatRegistry
    ) -> typing.Optional[Entity]:
        self.validate(obj)
        if obj is None:
            return None

        return self.inner_class.clone(obj, registry)


class List(CloneCat):
    """Class for cloning a list of instances.

    When an instance in the list is already copied,
    then it is not copied again, but the already copied instance is returned.

    Usage:
    1. Use directly with a class:
        some_attribute = Clone(List(SomeCloneCatClass))
    2. Use directly with an instance:
        some_attribute = Clone(List(Optional(SomeCloneCatClass)))
    3. With a string location to a class (useful for solving circular imports):
        some_attribute = Clone(List("your_package.SomeCloneCatClass"))
    """

    inspector_class = EmptyInspector

    class Meta:
        model = list

    def __init__(self, inner_class: typing.Union[CloneCat, type[CloneCat], str]):
        self._inner_class = inner_class

    @property
    def inner_class(self):
        if isinstance(self._inner_class, str):
            return import_clone_cat_class(self._inner_class)
        return self._inner_class

    def clone(self, obj: list[Entity], registry: CloneCatRegistry) -> list[Entity]:
        self.validate(obj)
        return [self.inner_class.clone(item, registry) for item in obj]


class Set(CloneCat):
    """Class for cloning a set of instances.

    When an instance in the set is already copied,
    then it is not copied again, but the already copied instance is returned.

    Usage:
    1. Use directly with a class:
        some_attribute = Clone(Set(SomeCloneCatClass))
    2. Use directly with an instance:
        some_attribute = Clone(Set(Optional(SomeCloneCatClass)))
    3. With a string location to a class (useful for solving circular imports):
        some_attribute = Clone(Set("your_package.SomeCloneCatClass"))
    """

    inspector_class = EmptyInspector

    class Meta:
        model = set

    def __init__(self, inner_class: typing.Union[CloneCat, type[CloneCat], str]):
        self._inner_class = inner_class

    @property
    def inner_class(self):
        if isinstance(self._inner_class, str):
            return import_clone_cat_class(self._inner_class)
        return self._inner_class

    def clone(self, obj: set[Entity], registry: CloneCatRegistry) -> set[Entity]:
        self.validate(obj)
        return {self.inner_class.clone(item, registry) for item in obj}


class OneOf(CloneCat):
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

    def __init__(self, *inner_classes: typing.Union[type[CloneCat], str]):
        super().__init__()
        self._inner_classes = inner_classes

    @property
    def inner_classes(self):
        classes = []
        for inner_class in self._inner_classes:
            if isinstance(inner_class, str):
                classes.append(import_clone_cat_class(inner_class))
            else:
                classes.append(inner_class)
        return classes

    def is_correct_type(self, obj: Entity) -> bool:
        return any(
            inner_class.is_correct_type(obj) for inner_class in self.inner_classes
        )

    def validate(self, obj: Entity) -> None:
        if not self.is_correct_type(obj):
            inner_classes = ",".join(
                str(inner_class) for inner_class in self.inner_classes
            )
            raise ValueError(
                f"Expected instance to be one of: {inner_classes}, " f"got {type(obj)}"
            )

    def clone(self, obj: Entity, registry: CloneCatRegistry) -> Entity:
        self.validate(obj)

        try:
            inner_class = next(
                inner_class
                for inner_class in self.inner_classes
                if inner_class.is_correct_type(obj)
            )
        except StopIteration:
            raise Exception(f"No class found for {obj.__class__}")

        return inner_class.clone(obj, registry)
