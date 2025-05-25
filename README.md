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
Think `copy.deepcopy()` but with superpowers and a sense of humor.

## 🚀 Why Twinly?

Ever tried to clone a complex object only to find that half its relationships went on vacation?
Twinly keeps the family together!
It's like a family reunion, but for your data structures.

# TODO: finish

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

# TODO: Complete

### Advanced Cloning with Options

# TODO: complete section

### Handling Circular References

# TODO: complete section

## 🎪 Advanced Features

# TODO: complete section

### Performance Monitoring

This section is a work in progress.

## 🔧 Configuration

Twinly can be configured globally or per-operation:

# TODO: complete section

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
