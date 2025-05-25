from tests.models import Foo
from twinly.inspectors.model import TwinlyModelBase
from twinly.registry import TwinlyRegistry


def test_ci() -> None:
    class CopyFoo(TwinlyModelBase):
        class Meta:
            model = Foo
            ignore = {Foo.id}
            copy = {Foo.bar}

    registry = TwinlyRegistry()
    new_foo = CopyFoo.clone(Foo(bar="bar"), registry=registry)
    assert new_foo.bar == "bar"
