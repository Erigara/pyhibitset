"""
Tests for pyhibitset
"""
from typing import Set

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, consumes
from pyhibitset import PyBitSet

index = st.integers(min_value=0, max_value=16777216)


@given(element=index)
def test_add(element: int):
    bitset = PyBitSet()
    assert not bitset.add(element)
    assert bitset.add(element)


@given(elements=st.sets(elements=index))
def test_add_many(elements: Set[int]):
    bitset = PyBitSet()
    for element in elements:
        assert not bitset.add(element)
        assert bitset.add(element)


@given(element=index)
def test_remove(element: int):
    bitset = PyBitSet()
    bitset.add(element)
    assert bitset.remove(element)
    assert not bitset.remove(element)


@given(element=index)
def test_contains(element: int):
    bitset = PyBitSet()
    assert not bitset.contains(element)
    bitset.add(element)
    assert bitset.contains(element)


@given(element=index)
def test_in(element: int):
    bitset = PyBitSet()
    assert element not in bitset
    bitset.add(element)
    assert element in bitset


@given(elements_1=st.sets(elements=index), elements_2=st.sets(elements=index))
def test_contains_set(elements_1: Set[int], elements_2: Set[int]):
    a = PyBitSet()
    b = PyBitSet()
    for element in elements_1:
        a.add(element)
    for element in elements_2:
        a.add(element)
        b.add(element)
    assert a.contains_set(b)


@given(elements=st.sets(elements=index))
def test_iter(elements: Set[int]):
    bitset = PyBitSet()
    for element in elements:
        bitset.add(element)

    # check that bitset is subset of elements
    for element in bitset:
        assert element in elements

    # check that elements is subset of bitset
    for element in elements:
        assert element in bitset


@given(elements=st.sets(elements=index))
def test_clear(elements: Set[int]):
    empty = PyBitSet()
    bitset = PyBitSet()
    for element in elements:
        bitset.add(element)
    bitset.clear()
    # check that bitset == empty
    # empty set contains only empty set
    assert empty.contains_set(bitset)


class SetComparison(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.bitset = PyBitSet()
        self.model = set()

    elements = Bundle("elements")

    @rule(target=elements, element=index)
    def add(self, element):
        self.model.add(element)
        self.bitset.add(element)
        return element

    @rule(element=consumes(elements))
    def remove(self, element):
        self.bitset.remove(element)
        self.model.remove(element)

    @rule()
    def values_agree(self):
        bitset = self.bitset
        model = self.model
        # check that bitset is subset of model
        for element in bitset:
            assert element in model

        # check that model is subset of bitset
        for element in model:
            assert element in bitset


TestSetComparison = SetComparison.TestCase
