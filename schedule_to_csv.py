#!/usr/bin/env python3

import json
import csv
import datetime
from pathlib import Path

def convert_schedule_to_csv():
    # Read the JSON file
    with open('schedule.json', 'r') as json_file:
        data = json.load(json_file)
    
    # Open a CSV file for writing
    with open('schedule.csv', 'w', newline='') as csv_file:
        # Create CSV writer
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        
        # Write header
        csv_writer.writerow(['Date', 'Start Time', 'End Time', 'Act Name', 'Stage Name'])
        
        # Get schedule days
        schedule = data.get('schedule', {})
        days = schedule.get('conference', {}).get('days', [])
        
        # Process each day
        for day in days:
            date = day.get('date')
            
            # Process each room in the day
            rooms = day.get('rooms', {})
            for room_name, events in rooms.items():
                # Process each event in the room
                for event in events:
                    title = event.get('title', '')
                    # Escape any commas in the title by wrapping in quotes
                    if ',' in title:
                        title = title.replace(',', '-')  # Escape any existing double quotes
                    
                    start_time = event.get('start', '')
                    
                    # Calculate end time
                    duration_str = event.get('duration', '00:00')
                    start_datetime = datetime.datetime.strptime(start_time, '%H:%M')
                    
                    # Parse duration (format is typically "HH:MM")
                    duration_parts = duration_str.split(':')
                    
                    # Handle special cases in duration
                    if len(duration_parts) == 2:
                        hours, minutes = map(int, duration_parts)
                    elif ':' not in duration_str and duration_str.endswith(':00'):
                        # Handle case like "1:05:00"
                        hours = int(duration_str.split(':')[0])
                        minutes = 0
                    else:
                        try:
                            # Try to handle non-standard formats
                            hours = int(duration_parts[0])
                            minutes = int(duration_parts[1]) if len(duration_parts) > 1 else 0
                        except ValueError:
                            hours, minutes = 0, 0
                    
                    # Calculate end datetime
                    end_datetime = start_datetime + datetime.timedelta(hours=hours, minutes=minutes)
                    end_time = end_datetime.strftime('%H:%M')
                    
                    # Write event to CSV with quotes around the act name
                    csv_writer.writerow([date, start_time, end_time, f'{title}', room_name])
    
    print(f"Conversion complete. CSV file saved as: schedule.csv")

if __name__ == "__main__":
    convert_schedule_to_csv()
