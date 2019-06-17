"""Custom types used to annotate functions and methods"""
from typing import List, TypeVar

Min = TypeVar('Min')
Max = TypeVar('Max')
NumClass = TypeVar('NumClass')  # it can be int, float, etc..
NumList = List[NumClass]
Error = TypeVar('Error')  # it represents an exception class like ValueError
