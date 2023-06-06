class UserInputHandler:
    def get_date_input(self):
        start_date_str = input("Enter the start date (MM/DD/YYYY), or press Enter for default: ").strip() or None
        end_date_str = input("Enter the end date (MM/DD/YYYY), or press Enter for default: ").strip() or None
        return start_date_str, end_date_str

    def get_plan_input(self, pricing_plans):
        print("Available Pricing Plans:")
        for i, plan in enumerate(pricing_plans, 1):
            print(f"{i}. {plan['name']}")
        selected_plan_index = int(input("Select a pricing plan (enter the number): ")) - 1
        return pricing_plans[selected_plan_index]
