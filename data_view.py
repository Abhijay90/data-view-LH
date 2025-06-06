#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

class DataView:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = None
        self.headers = [
            'initiatorName',
            'initiatorUid',
            'eventName',
            'eventClass',
            'eventStatus',
            'createdAt',
            'eventDate',
            'eventDescription',
            'otherReasonToClose',
            'id',
            'questionnaires',
            'updatedAt',
            'shareCloseMessage',
            'howManyPeople',
            'viewCount',
            'numberRemainingSpots',
            'numberAttending'
        ]
        self.load_data()

    def load_data(self):
        """Load data from JSON file and flatten events from all dates"""
        try:
            with open(self.json_file, 'r') as f:
                raw = json.load(f)
                # Flatten all events from all dates
                self.data = []
                if 'byDate' in raw:
                    for date in raw['byDate']:
                        date_data = raw['byDate'][date]
                        if 'events' in date_data:
                            for event in date_data['events']:
                                # Add date information to the event
                                if 'timing' in event and 'eventDate' in event['timing']:
                                    event['eventDate'] = event['timing']['eventDate']
                                if 'timing' in event and 'eventStartTime' in event['timing']:
                                    event['eventStartTime'] = event['timing']['eventStartTime']
                                if 'subscribeEvent' in event and 'viewCount' in event['subscribeEvent']:
                                    event['viewCount'] = event['subscribeEvent']['viewCount']
                                else:
                                    event['viewCount'] = ''
                                self.data.append(event)
                else:
                    self.data = []
                print("Loaded {} events from the JSON file".format(len(self.data)))
        except Exception as e:
            print("Error loading JSON file:", str(e))
            self.data = None

    def get_headers(self):
        """Get the specified headers"""
        return self.headers

    def get_data(self):
        """Get data for specified headers"""
        if not self.data:
            return []

        result = []
        for item in self.data:
            row = {}
            for header in self.headers:
                value = item.get(header, '')
                # Extract second value from howManyPeople array if it exists
                if header == 'howManyPeople' and isinstance(value, list) and len(value) > 1:
                    value = value[1]
                # Format date fields
                if header in ['createdAt', 'eventDate', 'updatedAt']:
                    value = self.format_date(value, header)
                row[header] = value
            result.append(row)
        return result

    def format_date(self, date_str, header=None):
        """Format date string to readable format"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            # For createdAt, only return the date
            if header == 'createdAt':
                return date_obj.strftime("%d/%m/%Y")
            # For other date fields, return full datetime
            return date_obj.strftime("%d/%m/%Y %H:%M:%S")
        except:
            return date_str

    def display_data(self):
        """Display data in a formatted table"""
        if not self.data:
            print("No data available")
            return

        # Print headers
        header_str = " | ".join(self.headers)
        separator = "=" * len(header_str)
        
        print("\n" + separator)
        print(header_str)
        print(separator)

        # Print data rows
        for item in self.data:
            if not isinstance(item, dict):
                continue  # Skip items that are not dictionaries
            row = []
            for header in self.headers:
                value = item.get(header, '')
                if header in ['createdAt', 'eventDate', 'updatedAt']:
                    value = self.format_date(value, header)
                # Ensure utf-8 encoding for Python 2
                try:
                    if isinstance(value, unicode):
                        value = value.encode('utf-8')
                    else:
                        value = str(value)
                except:
                    value = str(value)
                row.append(value)
            print(" | ".join(row))

def main():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(current_dir, 'data_files', 'event_details_1apr-2june.json')

    # Create DataView instance
    data_view = DataView(json_file)

    # Display data
    data_view.display_data()

    # Export to CSV
    from export_to_csv import export_events_to_csv
    export_events_to_csv(data_view.data, data_view.headers, output_filename='event_export_all.csv')

if __name__ == "__main__":
    main() 