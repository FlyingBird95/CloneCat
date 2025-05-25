import importlib
import inspect

from .twinly import Twinly


def import_copy_cat_class(dotted_path: str) -> type[Twinly]:
    """
    Dynamically import a class from a dotted module path.

    Parameters:
        dotted_path (str): The full dotted path to the class,
        e.g. "package.module.ClassName".

    Returns:
        type: The class object specified by the dotted path.

    Raises:
        ImportError: If the module cannot be imported.
        AttributeError: If the class is not found in the module.
    """
    module_path, class_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    copy_cat_class = getattr(module, class_name)
    if inspect.isclass(copy_cat_class):
        if not issubclass(copy_cat_class, Twinly):
            raise ValueError(
                f"Class imported at {dotted_path} is not a subclass of Twinly."
            )
    elif not isinstance(copy_cat_class, Twinly):
        raise ValueError(
            f"Class imported at {dotted_path} is not an instance of Twinly."
        )

    return copy_cat_class
