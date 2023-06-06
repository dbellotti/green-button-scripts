from collections import defaultdict
from datetime import datetime


class EnergyDataPrinter:
    def calculate_cost(self, time_totals, season_plan):
        return time_totals * season_plan

    def print_cost(self, title, time_totals, season_plan):
        print(f"{title}: \t{time_totals:.3f} kWh \t(Cost: ${self.calculate_cost(time_totals, season_plan):.2f})")

    def calculate_num_months(self, start_date, end_date):
        start_month = start_date.month
        end_month = end_date.month
        start_day = start_date.day
        end_day = end_date.day

        num_years = end_date.year - start_date.year
        num_months = num_years * 12

        if start_day > end_day:
            num_months += 1

        if end_day >= start_day:
            num_months += 1

        return num_months

    def print_totals_and_cost(self, totals, selected_plan):
        for date_range, season_totals in totals.items():
            start_date, end_date = date_range
            print(f"\nDate Range: {start_date.strftime('%m/%d/%Y')} - {end_date.strftime('%m/%d/%Y')}")

            for season, time_totals in season_totals.items():
                season_plan = selected_plan[season.lower()]
                print()
                print(season)
                self.print_cost("On", time_totals['On Peak'], season_plan['on_peak'])
                self.print_cost("Off", time_totals['Off Peak'], season_plan['off_peak'])
                self.print_cost("Super", time_totals['Super Off Peak'], season_plan['super_off_peak'])

            combined_total = sum(sum(time_totals.values()) for time_totals in season_totals.values())
            
            combined_cost = (
                sum(time_totals['On Peak'] * season_plan['on_peak'] for time_totals in season_totals.values())
                + sum(time_totals['Off Peak'] * season_plan['off_peak'] for time_totals in season_totals.values())
                + sum(time_totals['Super Off Peak'] * season_plan['super_off_peak'] for time_totals in season_totals.values())
                + (selected_plan['monthly_service_fee'] * self.calculate_num_months(start_date, end_date))
            )
            
            print(f"\nCombined Total: {combined_total:.3f} kWh (Cost: ${combined_cost:.2f})")

    def print_totals_and_cost_by_month(self, totals_by_month, selected_plan):
        net_generated = 0
        net_consumed = 0
        for month, month_totals in totals_by_month.items():
            monthly_total = sum(sum(time_totals.values()) for time_totals in month_totals.values())
            print(f"\nMonth: {month} ({monthly_total:.3f} kWh)")

            for season, season_totals in month_totals.items():
                season_plan = selected_plan[season.lower()]
                print()
                print(season)
                self.print_cost("On", season_totals['On Peak'], season_plan['on_peak'])
                self.print_cost("Off", season_totals['Off Peak'], season_plan['off_peak'])
                self.print_cost("Super", season_totals['Super Off Peak'], season_plan['super_off_peak'])

                if monthly_total < 0:
                    net_generated += monthly_total * -0.04
                    print(f"Generation Credit: ${monthly_total * -0.04:.2f}")
                else:
                    monthly_cost = (
                        sum(time_totals['On Peak'] * season_plan['on_peak'] for time_totals in month_totals.values())
                        + sum(time_totals['Off Peak'] * season_plan['off_peak'] for time_totals in month_totals.values())
                        + sum(time_totals['Super Off Peak'] * season_plan['super_off_peak'] for time_totals in month_totals.values())
                        + selected_plan['monthly_service_fee']
                    )
                    net_consumed += monthly_cost
                    print(f"Net Cost: ${monthly_cost:.2f}")

            combined_total = 0
            combined_cost = 0
            for month_totals in totals_by_month.values():
                combined_total += sum(sum(time_totals.values()) for time_totals in month_totals.values())
                combined_cost += (
                    sum(time_totals['On Peak'] * season_plan['on_peak'] for time_totals in month_totals.values())
                    + sum(time_totals['Off Peak'] * season_plan['off_peak'] for time_totals in month_totals.values())
                    + sum(time_totals['Super Off Peak'] * season_plan['super_off_peak'] for time_totals in month_totals.values())
                    + selected_plan['monthly_service_fee']
                )

        #print(f"\nCombined Total: {combined_total:.3f} kWh (Cost: ${combined_cost:.2f})")
        print(f"\nTotal Generation Credit: ${net_generated:.2f}")
        print(f"Total Net Cost: ${net_consumed:.2f}")
        print(f"Total True-Up Cost: ${net_consumed - net_generated:.2f}")
