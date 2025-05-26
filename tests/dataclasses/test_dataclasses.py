import pytest

from clonecat import CloneCat, CloneCatRegistry
from clonecat.inspectors.dataclass import DataclassInspector
from tests.dataclasses.models import Author


class CloneAuthor(CloneCat):
    inspector_class = DataclassInspector

    class Meta:
        model = Author


@pytest.mark.skip()
def test_clone_author():
    author = Author(first_name="first_name", last_name="last_name")
    new_author = CloneAuthor.clone(author, CloneCatRegistry())
    assert new_author is not author
    assert new_author.first_name == author.first_name
    assert new_author.last_name == author.last_name
