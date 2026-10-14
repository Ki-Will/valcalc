"""Input validation helpers for numeric data."""

import decimal

__all__ = [
    "ValidationError",
    "parse_number",
    "validate_float",
    "validate_int",
    "validate_non_negative",
    "validate_positive",
]


class ValidationError(ValueError):
    """Raised when a value does not pass validation.

    Subclasses :class:`ValueError` so it can be caught either narrowly or by
    generic ``except ValueError`` handlers.
    """


def parse_number(value, field="value"):
    """Return ``value`` as a ``float``.

    Accepts ``int``, ``float``, ``decimal.Decimal`` and ``str`` (whitespace and
    thousands separators are tolerated, e.g. ``"1,234.50"``). Raises
    :class:`ValidationError` for anything else, including ``bool`` and ``None``.
    """
    if isinstance(value, bool):
        raise ValidationError(f"{field} must be a number, got boolean {value!r}")
    if isinstance(value, (int, float, decimal.Decimal)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if not text:
            raise ValidationError(f"{field} must not be empty")
        try:
            return float(text)
        except ValueError:
            raise ValidationError(f"{field} must be a number, got {value!r}") from None
    raise ValidationError(
        f"{field} must be a number, got {type(value).__name__}"
    )


def validate_float(value, field="value"):
    """Return ``value`` as a ``float`` or raise :class:`ValidationError`."""
    return parse_number(value, field)


def validate_int(value, field="value"):
    """Return ``value`` as an ``int`` if it represents a whole number.

    >>> validate_int("7")
    7
    >>> validate_int("7.5", "quantity")   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    valcalc.validators.ValidationError: quantity must be a whole number, got '7.5'
    """
    number = parse_number(value, field)
    if not number.is_integer():
        raise ValidationError(f"{field} must be a whole number, got {value!r}")
    return int(number)


def validate_non_negative(value, field="value"):
    """Return ``value`` as a ``float`` if it is ``>= 0``."""
    number = parse_number(value, field)
    if number < 0:
        raise ValidationError(f"{field} must be >= 0, got {value!r}")
    return number


def validate_positive(value, field="value"):
    """Return ``value`` as a ``float`` if it is ``> 0``."""
    number = parse_number(value, field)
    if number <= 0:
        raise ValidationError(f"{field} must be > 0, got {value!r}")
    return number
