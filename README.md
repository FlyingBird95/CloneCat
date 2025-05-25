# 👯‍♀️ Twin

![CI](https://github.com/FlyingBird95/twin/workflows/CI/badge.svg)
![Release](https://github.com/FlyingBird95/twin/workflows/Release/badge.svg)
![PyPI version](https://badge.fury.io/py/twin.svg)
![Python versions](https://img.shields.io/pypi/pyversions/twin.svg)
![Downloads](https://pepy.tech/badge/twin)
![License](https://img.shields.io/github/license/FlyingBird95/twin.svg)
![Code coverage](https://codecov.io/gh/FlyingBird95/twin/branch/main/graph/badge.svg)

> *"Two heads are better than one, but two objects are just right!"*

**Twin** is a Python library that creates perfect copies of your objects along with all their relationships.
Think `copy.deepcopy()` but with superpowers and a sense of humor.

## 🚀 Why Twin?

Ever tried to clone a complex object only to find that half its relationships went on vacation?
Twin keeps the family together!
It's like a family reunion, but for your data structures.

```python
from twin import clone

# Your original object (let's call him Bob)
bob = ComplexObject(name="Bob", friends=[alice, charlie])

# Create Bob's twin (let's call her... Bob²)
bob_twin = clone(bob)

# They're identical but independent!
assert bob_twin.name == bob.name
assert bob_twin is not bob  # Different objects
assert bob_twin.friends[0] is not bob.friends[0]  # Even the friends are twins!
```

## ✨ Features

- 🔗 **Relationship Preservation**: Keeps all your object relationships intact
- 🏃‍♂️ **Blazing Fast**: Optimized for performance (okay, we tried our best)
- 🧠 **Smart Detection**: Automatically handles circular references without breaking a sweat
- 🎯 **Type Safe**: Full type hints because we're not animals
- 🛡️ **Battle Tested**: Comprehensive test suite (translation: we broke it many times)
- 🎭 **Customizable**: Supports custom cloning strategies for picky objects

## 📦 Installation

Using uv (because you're cool like that):

```bash
uv add twin
```

Or with pip (if you must):

```bash
pip install twin
```

## 🎮 Quick Start

### Basic Cloning

```python
from twin import clone

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.friends = []

# Create some people
alice = Person("Alice", 30)
bob = Person("Bob", 25)
alice.friends.append(bob)
bob.friends.append(alice)  # They're BFFs

# Clone Alice (and Bob comes along for the ride)
alice_twin = clone(alice)

print(f"Original Alice: {alice.name}")
print(f"Twin Alice: {alice_twin.name}")
print(f"Are they the same object? {alice is alice_twin}")  # False
print(f"Are their friends the same? {alice.friends[0] is alice_twin.friends[0]}")  # False
```

### Advanced Cloning with Options

```python
from twin import clone, CloneOptions

# For when you want more control
options = CloneOptions(
    deep=True,              # Deep clone everything (default)
    preserve_ids=False,     # Don't preserve object IDs
    max_depth=10,          # Prevent infinite recursion
    custom_handlers={       # Custom cloning for special objects
        MySpecialClass: my_special_cloner
    }
)

cloned_object = clone(original_object, options=options)
```

### Handling Circular References

```python
# Twin handles circular references like a boss
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []

root = Node("root")
child = Node("child")
root.children.append(child)
child.parent = root  # Circular reference!

# No problem for Twin!
root_twin = clone(root)
assert root_twin.children[0].parent is root_twin  # Relationships preserved!
```

## 🎪 Advanced Features

### Custom Clone Handlers

Sometimes your objects are special snowflakes that need special treatment:

```python
from twin import clone, register_handler

class DatabaseConnection:
    def __init__(self, url):
        self.url = url
        self.connection = create_connection(url)

def clone_db_connection(original):
    # Don't clone the actual connection, create a new one
    return DatabaseConnection(original.url)

register_handler(DatabaseConnection, clone_db_connection)

# Now your database connections will be properly handled
cloned_obj = clone(my_object_with_db_connection)
```

### Performance Monitoring

This section is a work in progress.

## 🔧 Configuration

Twin can be configured globally or per-operation:

```python
from twin import configure

# Global configuration
configure(
    default_depth=5,
    enable_logging=True,
    cache_clones=True  # Cache frequently cloned objects
)
```

## 🐛 Common Gotchas

1. **Lambda Functions**: Can't be pickled, can't be twinned. Sorry! 🤷‍♀️
2. **File Objects**: These are handle-based and don't play nice with cloning
3. **Thread Objects**: Threads are like pets - you can't just copy them
4. **Database Connections**: Use custom handlers for these bad boys

## 🧪 Testing

Run the test suite:

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov=twin --cov-report=html
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
