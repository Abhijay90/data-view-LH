import csv
import os
import sys
from datetime import datetime

if sys.version_info[0] < 3:
    import codecs

def format_date(date_str, header=None):
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        # For all date fields, return only the date
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str

def export_events_to_csv(events, headers, output_filename='event_export_joiner_less_than5.csv'):
    """
    Export a list of event dictionaries to a CSV file in the data_output folder.
    Args:
        events (list): List of event dictionaries.
        headers (list): List of headers/fields to export.
        output_filename (str): Name of the output CSV file.
    """
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, output_filename)
    if sys.version_info[0] < 3:
        # Python 2: open in binary mode and encode all values to utf-8
        with open(output_path, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for event in events:
                row = {}
                for header in headers:
                    value = event.get(header, '')
                    # Format date fields
                    if header in ['createdAt', 'eventDate', 'eventStartTime', 'updatedAt']:
                        value = format_date(value, header)
                    # Extract second value from howManyPeople array if it exists
                    if header == 'howManyPeople' and isinstance(value, list) and len(value) > 1:
                        value = value[1]
                    if isinstance(value, unicode):
                        value = value.encode('utf-8')
                    elif not isinstance(value, str):
                        value = str(value)
                    row[header] = value
                writer.writerow(row)
    else:
        # Python 3
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for event in events:
                row = {}
                for header in headers:
                    value = event.get(header, '')
                    # Format date fields
                    if header in ['createdAt', 'eventDate', 'eventStartTime', 'updatedAt']:
                        value = format_date(value, header)
                    # Extract second value from howManyPeople array if it exists
                    if header == 'howManyPeople' and isinstance(value, list) and len(value) > 1:
                        value = value[1]
                    row[header] = value
                writer.writerow(row)
    print("Exported {} events to {}".format(len(events), output_path)) 