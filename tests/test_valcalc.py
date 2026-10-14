"""Unit tests for the valcalc package (stdlib unittest only)."""

import decimal
import unittest

import valcalc
from valcalc import ValidationError


class ValidatorTests(unittest.TestCase):
    def test_parse_number_accepts_str_int_float_decimal(self):
        self.assertEqual(valcalc.parse_number(" 42 "), 42.0)
        self.assertEqual(valcalc.parse_number(7), 7.0)
        self.assertEqual(valcalc.parse_number(2.5), 2.5)
        self.assertEqual(valcalc.parse_number(decimal.Decimal("3.5")), 3.5)

    def test_parse_number_tolerates_thousands_separators(self):
        self.assertEqual(valcalc.parse_number("1,234.50"), 1234.5)

    def test_parse_number_rejects_garbage(self):
        for bad in ("abc", "", None, True, [1]):
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    valcalc.parse_number(bad, "price")

    def test_validate_int(self):
        self.assertEqual(valcalc.validate_int("7", "quantity"), 7)
        self.assertEqual(valcalc.validate_int(7.0, "quantity"), 7)
        with self.assertRaises(ValidationError):
            valcalc.validate_int("7.5", "quantity")

    def test_validate_non_negative_and_positive(self):
        self.assertEqual(valcalc.validate_non_negative(0, "stock"), 0.0)
        self.assertEqual(valcalc.validate_positive("9.99", "price"), 9.99)
        with self.assertRaises(ValidationError):
            valcalc.validate_non_negative(-5, "stock")
        with self.assertRaises(ValidationError):
            valcalc.validate_positive(0, "price")

    def test_error_message_names_the_field(self):
        with self.assertRaises(ValidationError) as ctx:
            valcalc.validate_int("lots", "quantity")
        self.assertIn("quantity", str(ctx.exception))


class CalculatorTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(valcalc.add(10, 20, 30), 60.0)
        self.assertEqual(valcalc.add(), 0.0)
        self.assertEqual(valcalc.subtract(50, 8), 42.0)
        self.assertEqual(valcalc.multiply(4, 2.5), 10.0)
        self.assertEqual(valcalc.divide(10, 4), 2.5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            valcalc.divide(1, 0)

    def test_percent_of(self):
        self.assertEqual(valcalc.percent_of(25, 200), 12.5)
        with self.assertRaises(ZeroDivisionError):
            valcalc.percent_of(5, 0)

    def test_apply_discount(self):
        self.assertEqual(valcalc.apply_discount(80, 25), 60.0)
        self.assertEqual(valcalc.apply_discount(50, 0), 50.0)
        with self.assertRaises(ValidationError):
            valcalc.apply_discount(50, 150)

    def test_total_with_tax(self):
        self.assertEqual(valcalc.total_with_tax(100, 15), 115.0)
        self.assertEqual(valcalc.total_with_tax(100), 100.0)
        with self.assertRaises(ValidationError):
            valcalc.total_with_tax(100, -1)

    def test_round_money_cleans_float_artifacts(self):
        self.assertEqual(valcalc.round_money(0.1 + 0.2), 0.3)
        self.assertEqual(valcalc.round_money("19.999"), 20.0)

    def test_clamp(self):
        self.assertEqual(valcalc.clamp(15, 0, 10), 10)
        self.assertEqual(valcalc.clamp(-3, 0, 10), 0)
        self.assertEqual(valcalc.clamp(5, 0, 10), 5)
        with self.assertRaises(ValidationError):
            valcalc.clamp(1, 10, 0)


if __name__ == "__main__":
    unittest.main()
