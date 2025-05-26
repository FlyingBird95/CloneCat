import pytest

from tests.dataclasses.models import Author
from twinly import Twinly, TwinlyRegistry
from twinly.inspectors.dataclass import DataclassInspector


class CopyAuthor(Twinly):
    inspector_class = DataclassInspector

    class Meta:
        model = Author


@pytest.mark.skip()
def test_copy_author():
    author = Author(first_name="first_name", last_name="last_name")
    new_author = CopyAuthor.clone(author, TwinlyRegistry())
    assert new_author is not author
    assert new_author.first_name == author.first_name
    assert new_author.last_name == author.last_name
