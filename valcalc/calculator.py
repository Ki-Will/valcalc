"""Simple calculator helpers built on validated numeric input."""

from .validators import ValidationError, parse_number

__all__ = [
    "add",
    "apply_discount",
    "clamp",
    "divide",
    "multiply",
    "percent_of",
    "round_money",
    "subtract",
    "total_with_tax",
]


def _num(value, field="value"):
    return parse_number(value, field)


def add(*values):
    """Sum any number of values.

    >>> add(10, 20, 30)
    60.0
    """
    total = 0.0
    for value in values:
        total += _num(value)
    return total


def subtract(a, b):
    """Return ``a - b``."""
    return _num(a) - _num(b)


def multiply(a, b):
    """Return ``a * b``."""
    return _num(a) * _num(b)


def divide(a, b):
    """Return ``a / b``. Raises ``ZeroDivisionError`` when ``b`` is zero."""
    divisor = _num(b, "divisor")
    if divisor == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return _num(a, "dividend") / divisor


def percent_of(part, whole):
    """Return which percent ``part`` is of ``whole``.

    >>> percent_of(25, 200)
    12.5
    """
    whole_number = _num(whole, "whole")
    if whole_number == 0:
        raise ZeroDivisionError("cannot compute a percentage of zero")
    return _num(part, "part") / whole_number * 100


def apply_discount(price, percent):
    """Return ``price`` with ``percent`` (0-100) taken off, rounded to cents."""
    price_number = _num(price, "price")
    percent_number = _num(percent, "percent")
    if not 0 <= percent_number <= 100:
        raise ValidationError(
            f"percent must be between 0 and 100, got {percent_number!r}"
        )
    return round_money(price_number * (1 - percent_number / 100))


def total_with_tax(subtotal, tax_rate=0.0):
    """Return ``subtotal`` plus ``tax_rate`` percent, rounded to cents.

    >>> total_with_tax(100, 15)
    115.0
    """
    subtotal_number = _num(subtotal, "subtotal")
    rate = _num(tax_rate, "tax_rate")
    if rate < 0:
        raise ValidationError(f"tax_rate must be >= 0, got {rate!r}")
    return round_money(subtotal_number * (1 + rate / 100))


def round_money(amount):
    """Round to 2 decimal places, cleaning up float artifacts.

    >>> round_money(0.1 + 0.2)
    0.3
    """
    return round(_num(amount, "amount"), 2)


def clamp(number, low, high):
    """Constrain ``number`` to the inclusive range ``[low, high]``.

    >>> clamp(15, 0, 10)
    10
    """
    number_value = _num(number, "number")
    low_value = _num(low, "low")
    high_value = _num(high, "high")
    if low_value > high_value:
        raise ValidationError(
            f"low ({low_value!r}) must not exceed high ({high_value!r})"
        )
    return min(max(number_value, low_value), high_value)
