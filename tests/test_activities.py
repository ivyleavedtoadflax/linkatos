import pytest
from linkatos import activities


def test_none_event():
    event = None
    assert activities.is_empty(event) is True


def test_len_zero_event():
    event = []
    assert activities.is_empty(event) is True