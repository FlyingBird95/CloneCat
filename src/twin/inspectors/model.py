from sqlalchemy import inspect

from ..attributes import Attribute, Copy, Ignore
from ..twin import Twin
from .base import AttributeType, Inspector


def get_names(items: set[Attribute]) -> set[str]:
    """Extract the names from a set of Twin attributes."""
    return {item.name for item in items}


def create_attribute(attr_class: type[AttributeType], name: str) -> AttributeType:
    """Helper function to create a new instance with a specific name."""

    obj = attr_class()
    obj.name = name
    return obj


class ModelInspector(Inspector):
    """Model inspector class to extract the Attributes from an SQLAlchemy model."""

    def __init__(self, class_to_inspect: type[Twin]):
        super().__init__(class_to_inspect)
        self.ignore_attributes: set[Ignore] = set()
        if hasattr(class_to_inspect.Meta, "ignore"):
            self.ignore_attributes = {
                create_attribute(Ignore, attr.key)
                for attr in class_to_inspect.Meta.ignore
            }

        self.copy_attributes: set[Copy] = set()
        if hasattr(class_to_inspect.Meta, "copy"):
            self.copy_attributes = {
                create_attribute(Copy, attr.key) for attr in class_to_inspect.Meta.copy
            }

        self.class_attributes: set[Attribute] = {
            value
            for attr in dir(class_to_inspect)
            if isinstance(value := getattr(class_to_inspect, attr, None), Attribute)
        }

        self.derived_attributes: set[Ignore] = set()
        for attr in (
            self.ignore_attributes | self.copy_attributes | self.class_attributes
        ):
            self.derived_attributes |= self.get_derived_attributes(attr)

    def get_derived_attributes(self, attr: Attribute) -> set[Attribute]:
        """Returns all derived attributes.

        Derived attributes are found based on relations or on composite types.

        For relations, it's enough to specify Book.author,
        which has a derived attribute Book.author_id.
        For composites, it's enough to specify Book.price,
        which also includes Book.price_cur and Book.price_amt.
        """
        inspector = inspect(self.meta_class.model)
        if attr.name in inspector.relationships:
            primary_key_names = (key.name for key in inspector.primary_key)
            return {
                create_attribute(Ignore, key)
                for column in inspector.relationships[attr.name].local_columns
                if (key := inspector.get_property_by_column(column).key)
                not in primary_key_names
            }

        if attr.name in inspector.composites:
            primary_key_names = (key.name for key in inspector.primary_key)
            return {
                create_attribute(type(attr), column.name)
                for column in inspector.composites[attr.name].columns
                if column.name not in primary_key_names
            }
        return set()  # Not a relationship, nor composite

    def validate(self) -> None:
        """Validate whether the class attributes are defined properly."""

        # Validate in both Meta.ignore and as a class attribute
        if defined_in_both_places := get_names(self.ignore_attributes) & get_names(
            self.class_attributes
        ):
            attributes = ", ".join(sorted(defined_in_both_places))
            raise Exception(
                f"Duplicate attributes defined found in "
                f"Meta.ignore and on class: {attributes}"
            )

        # Validate in both Meta.copy and as a class attribute
        if defined_in_both_places := get_names(self.copy_attributes) & get_names(
            self.class_attributes
        ):
            attributes = ", ".join(sorted(defined_in_both_places))
            raise Exception(
                f"Duplicate attributes defined found in "
                f"Meta.copy and on class: {attributes}"
            )

        # Validate in both Meta.copy and in Meta.ignore
        if defined_in_both_places := get_names(self.copy_attributes) & get_names(
            self.ignore_attributes
        ):
            attributes = ", ".join(sorted(defined_in_both_places))
            raise Exception(
                f"Some attributes are defined in both "
                f"Meta.ignore and Meta.copy: {attributes}"
            )

        # Validate in both derived attributes and Meta.copy
        if defined_in_both_places := get_names(self.derived_attributes) & get_names(
            self.copy_attributes
        ):
            attributes = ", ".join(sorted(defined_in_both_places))
            raise Exception(
                f"Some attributes are derived automatically, "
                f"but they are also defined in Meta.copy: {attributes}"
            )

        # Validate in both derived attributes and Meta.ignore
        if defined_in_both_places := get_names(self.derived_attributes) & get_names(
            self.ignore_attributes
        ):
            attributes = ", ".join(sorted(defined_in_both_places))
            raise Exception(
                f"Some attributes are derived automatically, "
                f"but they are also defined in Meta.ignore: {attributes}"
            )

        # Validate in both derived attributes and on class level
        if defined_in_both_places := get_names(self.derived_attributes) & get_names(
            self.class_attributes
        ):
            attributes = ", ".join(sorted(defined_in_both_places))
            raise Exception(
                f"Some attributes are derived automatically, "
                f"but they are also defined on class: {attributes}"
            )

        # Validate unknown attributes
        if (
            unknown_attributes := get_names(self.all_twin_attributes)
            - self.get_model_attributes()
        ):
            attributes = ", ".join(sorted(unknown_attributes))
            raise Exception(f"Unknown attributes: {attributes}")

        # Validate missing attributes
        if missing_attributes := self.get_model_attributes() - get_names(
            self.all_twin_attributes
        ):
            attributes = ", ".join(sorted(missing_attributes))
            raise Exception(f"Missing attributes: {attributes}")

    def get_model_attributes(self) -> set[str]:
        """Get attributes by inspecting the SQLA model."""
        inspector = inspect(self.meta_class.model)
        return set(inspector.attrs.keys())

    @property
    def all_twin_attributes(self) -> set[Attribute]:
        """Returns all twin attributes."""
        return (
            self.copy_attributes
            | self.ignore_attributes
            | self.class_attributes
            | self.derived_attributes
        )


class TwinBase(Twin):
    """Base class for Twin classes that copies SQLAlchemy objects."""

    inspector_class = ModelInspector
