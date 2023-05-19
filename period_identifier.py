from datetime import datetime

class PeriodIdentifier:
    def __init__(self, holidays):
        self.holidays = holidays
        self.is_weekend = False
        self.is_holiday = False
        self.is_super_off_peak = False
        self.is_on_peak = False

    def identify_period(self, date, start_time):
        self.is_weekend = date.weekday() >= 5
        self.is_holiday = date.strftime("%m/%d/%Y") in self.holidays

        if self.is_weekend or self.is_holiday:
            self.is_super_off_peak = start_time < datetime.strptime("2:00 PM", "%I:%M %p").time()
        else:
            month = date.strftime("%B")
            self.is_super_off_peak = (
                month in ["March", "April"]
                and start_time >= datetime.strptime("10:00 AM", "%I:%M %p").time()
                and start_time < datetime.strptime("2:00 PM", "%I:%M %p").time()
            ) or (start_time < datetime.strptime("6:00 AM", "%I:%M %p").time())

        self.is_on_peak = (
            start_time >= datetime.strptime("4:00 PM", "%I:%M %p").time()
            and start_time < datetime.strptime("9:00 PM", "%I:%M %p").time()
        )

    def get_period(self):
        if self.is_on_peak:
            return "On Peak"
        elif self.is_super_off_peak:
            return "Super Off Peak"
        else:
            return "Off Peak"