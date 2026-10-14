# valcalc

Tiny **validation + calculator** toolkit for numeric input. Zero dependencies.

Install (from TestPyPI):

```bash
pip install valcalc --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple
```

## Validation

```python
import valcalc

valcalc.validate_int("42", "quantity")          # -> 42
valcalc.validate_positive("9.99", "price")     # -> 9.99
valcalc.validate_non_negative(0, "stock")      # -> 0.0
valcalc.parse_number("1,234.50")               # -> 1234.5

valcalc.validate_int("abc", "quantity")        # -> valcalc.ValidationError
valcalc.validate_non_negative(-5, "stock")     # -> valcalc.ValidationError
```

All validators raise `valcalc.ValidationError` (a `ValueError` subclass) with a
message that names the offending field, so they drop straight into form code.

## Calculations

```python
valcalc.add(10, 20, 30)            # -> 60.0
valcalc.subtract(50, 8)            # -> 42.0
valcalc.multiply(4, 2.5)           # -> 10.0
valcalc.divide(10, 4)              # -> 2.5
valcalc.percent_of(25, 200)        # -> 12.5
valcalc.apply_discount(80, 25)     # -> 60.0
valcalc.total_with_tax(100, 15)    # -> 115.0
valcalc.round_money(0.1 + 0.2)     # -> 0.3
valcalc.clamp(15, 0, 10)           # -> 10
```

Division by zero raises `ZeroDivisionError`; a percentage or tax rate outside
`0..100` raises `ValidationError`.

## Tests

```bash
python -m unittest -v
```

## Used by

The `shop_inventory` Django project in this workspace uses `valcalc` for
product form validation and for stock totals rendered in its templates.
