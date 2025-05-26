"""
Twinly

This is a Python library
that creates perfect copies of your objects along with all their relationships.
"""
from twinly.attributes import Clone
from twinly.registry import TwinlyRegistry
from twinly.twinly import Twinly

__version__ = "0.1.14"
__author__ = "Patrick"

__all__ = [
    Clone,
    Twinly,
    TwinlyRegistry,
]
