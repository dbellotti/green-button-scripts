import unittest
from datetime import datetime, time
from period_identifier import PeriodIdentifier


class TestPeriodIdentifier(unittest.TestCase):
    def setUp(self):
        holidays = ["01/01/2023", "07/04/2023", "12/25/2023"]
        self.period_identifier = PeriodIdentifier(holidays)

    def test_identify_period_super_off_peak(self):
        date = datetime(2023, 5, 22)  # Monday
        start_time = time(1, 0)  # 1:00 AM
        self.period_identifier.identify_period(date, start_time)
        period = self.period_identifier.get_period()
        self.assertEqual(period, "Super Off Peak")

    def test_identify_period_on_peak(self):
        date = datetime(2023, 5, 22)  # Monday
        start_time = time(18, 0)  # 6:00 PM
        self.period_identifier.identify_period(date, start_time)
        period = self.period_identifier.get_period()
        self.assertEqual(period, "On Peak")

    def test_identify_period_off_peak(self):
        date = datetime(2023, 5, 22)  # Monday
        start_time = time(10, 0)  # 10:00 AM
        self.period_identifier.identify_period(date, start_time)
        period = self.period_identifier.get_period()
        self.assertEqual(period, "Off Peak")

    def test_identify_period_super_off_peak_weekend(self):
        date = datetime(2023, 5, 27)  # Saturday
        start_time = time(12, 0)  # 12:00 PM
        self.period_identifier.identify_period(date, start_time)
        period = self.period_identifier.get_period()
        self.assertEqual(period, "Super Off Peak")

    def test_identify_period_super_off_peak_holiday(self):
        date = datetime(2023, 7, 4)  # Independence Day
        start_time = time(9, 0)  # 9:00 AM
        self.period_identifier.identify_period(date, start_time)
        period = self.period_identifier.get_period()
        self.assertEqual(period, "Super Off Peak")


if __name__ == "__main__":
    unittest.main()
