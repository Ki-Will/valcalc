"""valcalc - tiny validation + calculation toolkit for numeric input.

>>> import valcalc
>>> valcalc.validate_int("42", "quantity")
42
>>> valcalc.total_with_tax(100, 15)
115.0
"""

from .calculator import (
    add,
    apply_discount,
    clamp,
    divide,
    multiply,
    percent_of,
    round_money,
    subtract,
    total_with_tax,
)
from .validators import (
    ValidationError,
    parse_number,
    validate_float,
    validate_int,
    validate_non_negative,
    validate_positive,
)

__version__ = "0.1.0"

__all__ = [
    "ValidationError",
    "add",
    "apply_discount",
    "clamp",
    "divide",
    "multiply",
    "parse_number",
    "percent_of",
    "round_money",
    "subtract",
    "total_with_tax",
    "validate_float",
    "validate_int",
    "validate_non_negative",
    "validate_positive",
    "__version__",
]
