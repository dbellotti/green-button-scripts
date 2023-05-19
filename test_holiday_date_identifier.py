import datetime
import pytest
from holiday_date_identifier import HolidayDateIdentifier

def test_get_holiday_date():
    # Create an instance of the HolidayDateIdentifier class
    holiday_identifier = HolidayDateIdentifier()

    # Test New Year's Day for 2023
    new_years_day_2023 = holiday_identifier.get_holiday_date("New Year's Day", 2023)
    assert new_years_day_2023 == datetime.date(2023, 1, 1)

    # Test Independence Day for 2022
    independence_day_2022 = holiday_identifier.get_holiday_date("Independence Day", 2022)
    assert independence_day_2022 == datetime.date(2022, 7, 4)

    # Test Thanksgiving Day for 2025
    thanksgiving_day_2025 = holiday_identifier.get_holiday_date("Thanksgiving Day", 2025)
    assert thanksgiving_day_2025 == datetime.date(2025, 11, 27)

def test_get_holidays_in_date_range():
    # Create an instance of the HolidayDateIdentifier class
    holiday_identifier = HolidayDateIdentifier()

    # Define the start and end datetimes
    start_datetime = datetime.datetime(2023, 1, 1)
    end_datetime = datetime.datetime(2025, 12, 31)

    # Get the holidays in the date range
    holidays = holiday_identifier.get_holidays_in_date_range(start_datetime, end_datetime)

    # Check the holidays
    assert holidays == [
        datetime.datetime(2023, 1, 1),
        datetime.datetime(2023, 2, 20),
        datetime.datetime(2023, 5, 29),
        datetime.datetime(2023, 7, 4),
        datetime.datetime(2023, 9, 4),
        datetime.datetime(2023, 11, 11),
        datetime.datetime(2023, 11, 23),
        datetime.datetime(2023, 12, 25),
        datetime.datetime(2024, 1, 1),
        datetime.datetime(2024, 2, 19),
        datetime.datetime(2024, 5, 27),
        datetime.datetime(2024, 7, 4),
        datetime.datetime(2024, 9, 2),
        datetime.datetime(2024, 11, 11),
        datetime.datetime(2024, 11, 28),
        datetime.datetime(2024, 12, 25),
        datetime.datetime(2025, 1, 1),
        datetime.datetime(2025, 2, 17),
        datetime.datetime(2025, 5, 26),
        datetime.datetime(2025, 7, 4),
        datetime.datetime(2025, 9, 1),
        datetime.datetime(2025, 11, 11),
        datetime.datetime(2025, 11, 27),
        datetime.datetime(2025, 12, 25)
    ]

# Run the tests
pytest.main()
