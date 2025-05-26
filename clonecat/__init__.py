"""
CloneCat

A Python framework that helps you create perfect clones of your objects
along with all their relationships.
"""
from clonecat.attributes import Clone
from clonecat.clonecat import CloneCat
from clonecat.registry import CloneCatRegistry

__version__ = "0.1.16"
__author__ = "Patrick"

__all__ = [
    Clone,
    CloneCat,
    CloneCatRegistry,
]
