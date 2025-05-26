from clonecat.inspectors.model import CloneCatModelBase
from clonecat.registry import CloneCatRegistry
from tests.models import Foo


def test_ci() -> None:
    class CloneFoo(CloneCatModelBase):
        class Meta:
            model = Foo
            ignore = {Foo.id}
            copy = {Foo.bar}

    registry = CloneCatRegistry()
    new_foo = CloneFoo.clone(Foo(bar="bar"), registry=registry)
    assert new_foo.bar == "bar"
