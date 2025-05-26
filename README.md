# 👯‍♀️ Twinly

![CI](https://github.com/FlyingBird95/twinly/workflows/CI/badge.svg)
![Release](https://github.com/FlyingBird95/twinly/workflows/Release/badge.svg)
![PyPI version](https://badge.fury.io/py/twinly.svg)
![Python versions](https://img.shields.io/pypi/pyversions/twinly.svg)
![Downloads](https://pepy.tech/badge/twinly)
![License](https://img.shields.io/github/license/FlyingBird95/twinly.svg)
![Code coverage](https://codecov.io/gh/FlyingBird95/twinly/branch/main/graph/badge.svg)

> *"Two heads are better than one, but two objects are just right!"*

**Twinly** is a Python library that creates perfect copies of your objects along with all their relationships.
Think `copy.deepcopy()` but with superpowers.

## 🚀 Why Twinly?

Ever tried to clone a complex object only to find that half its relationships went on vacation?
Twinly keeps the family together!
It's like a family reunion, but for your data structures.

Twinly has a clear interface to determine which relations should be copied,
which relations should be cloned,
and which relations should be ignored.

Additionally, Twinly has built in validation that verifies that all relations in a dataclass are specified.
When any attribute is left out, its corresponding Twinly class cannot be used.

Twinly works great with:
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Django models](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- More frameworks can be added easily. See documentation below.

## ✨ Features

- 🔗 **Relationship Preservation**: Keeps all your object relationships intact
- 🏃‍♂️ **Blazing Fast**: Optimized for performance (okay, we tried our best)
- 🧠 **Smart Detection**: Automatically handles circular references without breaking a sweat
- 🎯 **Type Safe**: Full type hints because we're not animals
- 🛡️ **Battle Tested**: Comprehensive test suite (translation: we broke it many times)
- 🎭 **Customizable**: Supports custom cloning strategies for picky objects

## 📦 Installation

Using `uv` (because you're cool like that):

```bash
uv add twinly
```

Or with pip (if you must):

```bash
pip install twinly
```

## 🎮 Quick Start

### Basic Cloning

Given the following dataclasses:

```python
import dataclasses

@dataclasses.dataclass
class Person:
    id: int
    first_name: str
    last_name: str



```

When a person must be cloned (don't try this at home),
use the following `Twinly` class:
```python
from twinly import Twinly
from twinly.inspectors.dataclass import DataclassInspector


class CopyPerson(Twinly):
    inspector_class = DataclassInspector
    class Meta:
        model = Person
        ignore = {"id"}
        copy = {"first_name", "last_name"}
```

Let's break down the snippet above into several chunks:
- `class CopyPerson(Twinly)`: All copy classes must inherit from `Twinly`.
- `inspector_class = DataclassInspector`: This tells `Twinly` how to interspect the dataclass, revealing its attributes.
- `class Meta`: A `Meta`-class is required, with at least the `model`-parameter set.
- `ignore = {"id"}`: Optionally: specify keys that should **NOT** be copied.
- `copy = {"first_name", "last_name"}`: Optionally specify keys that should be copied.

Given an instance of `Person` (yes, also [Elon Musk is human](https://cleantechnica.com/2020/05/14/elon-musk-is-only-human/)), clone this using:

```python
elon_musk = Person(first_name="Elon", last_name="Musk")
elon_musk_clone = CopyPerson.clone(elon_musk, TwinlyRegistry())
```

Forgot to say, but `TwinlyRegistry()` can be used
to keep track which new instances are created out of the existing instances.
It's nothing more than a glorified dictionary.

After cloning, the following assertions hold:
```python
assert elon_musk.first_name == elon_musk_clone.first_name
assert elon_musk.last_name == elon_musk_clone.last_name

# ID is not copied, and therefore different:
assert elon_musk.id != elon_musk_clone.id
```

### Advanced Cloning
Ignoring keys and copying are two options, but there is another one: cloning.
This implies that a new instance is created out of the old instance.
The relation remains intact.

Let's say Elon Musk favorite food is [Pineapple Pizza](https://voi.id/en/lifestyle/460104).
This is encoded with the following dataclasses:

```python
import dataclasses


@dataclasses.dataclass
class Food:
    name: str


@dataclasses.dataclass
class Person:
    id: int
    first_name: str
    last_name: str
```

And the corresponding `Twinly` models:

```python
from twinly import Twinly
from twinly.inspectors.dataclass import DataclassInspector

class CopyFood(Twinly):
    inspector_class = DataclassInspector
    class Meta:
        model = Food
        copy = {"name"}

class CopyPerson(Twinly):
    inspector_class = DataclassInspector
    class Meta:
        model = Person
        ignore = {"id"}
        copy = {"first_name", "last_name"}

    favorite_food: Food
```

Now, it's time to show how this can be cloned:

```python
pineapple_pizza = Food(name="Pineapple pizza")
elon_musk = Person(first_name="Elon", last_name="Musk", favorite_food=pineapple_pizza)
elon_musk_clone = CopyPerson.clone(elon_musk, TwinlyRegistry())
```

Trust, but verify:
```python
assert elon_musk.first_name == elon_musk_clone.first_name
assert elon_musk.last_name == elon_musk_clone.last_name

# Food is a different instance
assert elon_musk.favorite_food is not elon_musk_clone.favorite_food

# But they both love Pineapple Pizza
assert elon_musk.favorite_food.name == elon_musk_clone.favorite_food.name
```

### Handling Circular References

# TODO: complete section

## 🎪 Advanced Features

# TODO: complete section

### Performance Monitoring

This section is a work in progress.

# TODO: complete section


## 🧪 Testing

Run the test suite:

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov=twinly --cov-report=html
```

## 🤝 Contributing

We love contributions! Whether it's:

- 🐛 Bug reports
- 💡 Feature requests
- 📖 Documentation improvements
- 🧪 Test cases
- 🎨 Code improvements

Check out our [Contributing Guide](CONTRIBUTING.md) to get started.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the frustrations of `copy.deepcopy()`
- Built with love, coffee, and questionable life choices
- Special thanks to all the objects that sacrificed themselves during testing
