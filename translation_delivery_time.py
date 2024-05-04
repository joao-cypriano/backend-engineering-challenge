import json
import argparse
from collections import deque
from datetime import datetime, timedelta

def parse_args():
    parser = argparse.ArgumentParser(description='Calculate moving average of translation delivery time')
    parser.add_argument('--input_file', type=str, help='Input JSON file path')
    parser.add_argument('--window_size', type=int, help='Window size for moving average calculation')
    return parser.parse_args()

def calculate_moving_average(events, window_size):
    window = deque()
    output = []

    start_time = datetime.strptime(events[0]['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
    end_time = datetime.strptime(events[-1]['timestamp'], '%Y-%m-%d %H:%M:%S.%f')

    current_time = start_time
    while current_time <= end_time:
        events_in_window = [event for event in window if current_time - timedelta(minutes=window_size) <= event[0] <= current_time]
        if events_in_window:
            window_events = [event[1] for event in events_in_window]
            average_delivery_time = sum(window_events) / len(window_events)
            output.append({'date': current_time.strftime('%Y-%m-%d %H:%M:00'), 'average_delivery_time': average_delivery_time})
        else:
            output.append({'date': current_time.strftime('%Y-%m-%d %H:%M:00'), 'average_delivery_time': 0})

        current_time += timedelta(minutes=1)

        # Add events to the window that fall within the current minute
        while events and datetime.strptime(events[0]['timestamp'], '%Y-%m-%d %H:%M:%S.%f') <= current_time:
            event = events.pop(0)
            timestamp = datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            duration = event['duration']
            window.append((timestamp, duration))

        # Remove events that are outside the window
        while window and current_time - window[0][0] >= timedelta(minutes=window_size):
            window.popleft()

    return output



def main():
    args = parse_args()

    with open(args.input_file, 'r') as file:
        events = [json.loads(line) for line in file]

    events.sort(key=lambda x: x['timestamp'])
    output = calculate_moving_average(events, args.window_size)

    for line in output:
        print(json.dumps(line))

if __name__ == "__main__":
    main()
