import json
import os

json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_files', 'event_details_close_count.json')

def count_events(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    total = 0
    if 'byDate' in data:
        for date in data['byDate']:
            date_data = data['byDate'][date]
            if 'events' in date_data:
                total += len(date_data['events'])
    return total

if __name__ == '__main__':
    total_events = count_events(json_file)
    print('Total events in JSON file:', total_events) 