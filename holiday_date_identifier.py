import datetime

class HolidayDateIdentifier:
    def __init__(self):
        pass

    def _get_next_weekday(self, date, weekday):
        days_ahead = (weekday - date.weekday() + 7) % 7
        return date + datetime.timedelta(days=days_ahead)

    def get_holiday_date(self, holiday_name, year):
        if holiday_name == "New Year's Day":
            return datetime.date(year, 1, 1)
        elif holiday_name == "President's Day":
            first_day = datetime.date(year, 2, 1)
            return self._get_next_weekday(first_day, 0) + datetime.timedelta(weeks=2)
        elif holiday_name == "Memorial Day":
            last_day = datetime.date(year, 5, 31)
            return self._get_next_weekday(last_day, 0) - datetime.timedelta(weeks=1)
        elif holiday_name == "Independence Day":
            return datetime.date(year, 7, 4)
        elif holiday_name == "Labor Day":
            first_day = datetime.date(year, 9, 1)
            return self._get_next_weekday(first_day, 0)
        elif holiday_name == "Veterans Day":
            return datetime.date(year, 11, 11)
        elif holiday_name == "Thanksgiving Day":
            first_day = datetime.date(year, 11, 1)
            return self._get_next_weekday(first_day, 3) + datetime.timedelta(weeks=3)
        elif holiday_name == "Christmas Day":
            return datetime.date(year, 12, 25)
        else:
            return None

    def get_holidays_in_date_range(self, start_datetime, end_datetime):
        start_year = start_datetime.year
        end_year = end_datetime.year
        holidays = []

        for year in range(start_year, end_year + 1):
            for holiday_name in [
                "New Year's Day",
                "President's Day",
                "Memorial Day",
                "Independence Day",
                "Labor Day",
                "Veterans Day",
                "Thanksgiving Day",
                "Christmas Day"
            ]:
                holiday_date = self.get_holiday_date(holiday_name, year)
                if holiday_date and start_datetime <= datetime.datetime.combine(holiday_date, datetime.time()) <= end_datetime:
                    holidays.append(datetime.datetime.combine(holiday_date, datetime.time()))

        return holidays