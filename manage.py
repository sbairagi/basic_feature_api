#!/usr/bin/env python
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
    
    
    
from datetime import timedelta, datetime

def generate_lead_scores(start_date, end_date, total_target, frequency, day_of_delivery):
    lead_scores = {}
    current_date = start_date
    leads_per_schedule = total_target // ((end_date - start_date).days // frequency + 1)
    remaining_leads = total_target % ((end_date - start_date).days // frequency + 1)

    while current_date <= end_date:
        if current_date.weekday() == day_of_delivery:
            lead_scores[current_date.strftime('%Y-%m-%d')] = leads_per_schedule

        current_date += timedelta(days=frequency)

    # Distribute remaining leads starting from the first scheduled date
    current_date = start_date
    while remaining_leads > 0:
        if current_date.weekday() == day_of_delivery:
            lead_scores[current_date.strftime('%Y-%m-%d')] += 1
            remaining_leads -= 1

        current_date += timedelta(days=frequency)

    return lead_scores

# Example usage:
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
total_target = 15
frequency = 7  # Number of days between each delivery
day_of_delivery = 2  # Assuming 0 is Monday, 1 is Tuesday, and so on

result = generate_lead_scores(start_date, end_date, total_target, frequency, day_of_delivery)
print(result)

