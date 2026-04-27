import pytest
from datetime import date, timedelta
from expense_tracker.validators import (
    validate_date,
    validate_non_empty_str,
    validate_positive_float,
)


class TestValidateDate:
    def test_valid_date(self):
        assert validate_date("2024-09-18") == "2024-09-18"

    def test_strips_whitespace(self):
        assert validate_date("  2024-09-18  ") == "2024-09-18"

    def test_wrong_format_raises(self):
        with pytest.raises(ValueError, match="Invalid date format"):
            validate_date("18-09-2024")

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            validate_date("   ")

    def test_invalid_day_raises(self):
        with pytest.raises(ValueError, match="Invalid date format"):
            validate_date("2024-02-30")

    def test_future_date_raises(self):
        future = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        with pytest.raises(ValueError, match="in the future"):
            validate_date(future)

    def test_today_is_valid(self):
        today = date.today().strftime("%Y-%m-%d")
        assert validate_date(today) == today


class TestValidatePositiveFloat:
    def test_valid_value(self):
        assert validate_positive_float("15.50") == 15.5

    def test_rounds_to_2dp(self):
        assert validate_positive_float("9.999") == 10.0

    def test_zero_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            validate_positive_float("0")

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            validate_positive_float("-5")

    def test_non_numeric_raises(self):
        with pytest.raises(ValueError, match="Invalid number"):
            validate_positive_float("abc")


class TestValidateNonEmptyStr:
    def test_valid_value(self):
        assert validate_non_empty_str("  hello  ") == "hello"

    def test_blank_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            validate_non_empty_str("   ")

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            validate_non_empty_str("")
