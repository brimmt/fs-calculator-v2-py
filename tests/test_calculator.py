import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import unittest
from calculator_logic import Calculate


@pytest.fixture
def calc():
    return Calculate(5, 5)


def test_addition(calc):
    assert calc.add() == 10


def test_subtraction(calc):
    assert calc.subtract() == 0


def test_multiplication(calc):
    assert calc.multiply() == 25


def test_division(calc):
    assert calc.divide() == 1


def test_power(calc):
    assert calc.power() == 3125
