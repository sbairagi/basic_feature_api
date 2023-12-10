hi#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalapi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    
    
    
from datetime import datetime, timedelta

def calculate_delivery_schedule(start, end, total_target, frequency, delivery_days):
    delivery_schedule = {}
    
    current_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    
    while current_date <= end_date:
        if current_date.strftime("%A") in delivery_days:
            delivery_schedule[current_date.strftime("%Y-%m-%d")] = total_target / len(delivery_days)
            
        if frequency == "weekly":
            current_date += timedelta(weeks=1)
        elif frequency == "biweekly":
            current_date += timedelta(weeks=2)
        elif frequency == "monthly":
            current_date = (current_date + timedelta(days=31)).replace(day=1)
        elif frequency == "quarterly":
            current_date = (current_date + timedelta(days=92)).replace(day=1)
        elif frequency == "halfyearly":
            current_date = (current_date + timedelta(days=183)).replace(day=1)
        elif frequency == "yearly":
            current_date = current_date.replace(day=1, month=1, year=current_date.year + 1)
        else:
            current_date += timedelta(days=1)
    
    return delivery_schedule

# Example usage:
start_date = "2023-01-01"
end_date = "2023-12-31"
total_target = 100
frequency = "weekly"
delivery_days = ["Monday", "Tuesday"]

result = calculate_delivery_schedule(start_date, end_date, total_target, frequency, delivery_days)
print(result)