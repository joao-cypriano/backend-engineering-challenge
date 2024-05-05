import json
import argparse
from datetime import datetime, timedelta

def parse_args():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    # Create an ArgumentParser object to handle command-line arguments
    parser = argparse.ArgumentParser(description='Calculate moving average of translation delivery time')

    # Add arguments for input file and window size
    parser.add_argument('--input_file', type=str, help='Input JSON file path')
    parser.add_argument('--window_size', type=int, help='Window size for moving average calculation')

    # Parse the command-line arguments
    return parser.parse_args()

def calculate_moving_average(events, window_size):
    """
    Calculate the moving average of translation delivery time.

    Args:
        events (list): List of translation events.
        window_size (int): Size of the moving window for calculating the average.

    Returns:
        dict: Dictionary containing timestamps as keys and corresponding average delivery times.
    """

    # Get the start time and end time of the event data
    start_time = datetime.strptime(events[0]['timestamp'], '%Y-%m-%d %H:%M:%S.%f').replace(second=0, microsecond=0) # Start the time as the first full minute before the first event
    end_time = datetime.strptime(events[-1]['timestamp'], '%Y-%m-%d %H:%M:%S.%f').replace(second=0, microsecond=0) + timedelta(minutes=1) # End the window after the last minute is finished
    events_by_time = {} # Dictionary to store events grouped by time

    # Iterate through each translation event
    for event in events:
        window_counter = 0

        # Organize event timestamps usage to reduce redundancy
        event_timestamp = datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        replaced_event_timestamp = event_timestamp.replace(second=0, microsecond=0)
        formatted_replaced_event_timestamp = replaced_event_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Treat timestamps that are exactly on the minute mark (should enter that minute calculation) and that are after the minute mark (should enter the next minute calculation)
        if event_timestamp != replaced_event_timestamp:
            event_time = replaced_event_timestamp + timedelta(minutes=1)

            # Treat the first event if it's after the exact minute mark
            if event == events[0]:
                events_by_time[formatted_replaced_event_timestamp] = [0]
        else:
            event_time = formatted_replaced_event_timestamp
        duration = event['duration']

        # Distribute the event duration across the time window
        while event_time <= end_time and window_counter < window_size:
            if event_time.strftime("%Y-%m-%d %H:%M:%S") in events_by_time:
                events_by_time[event_time.strftime("%Y-%m-%d %H:%M:%S")].append(duration)
            else:
                events_by_time[event_time.strftime("%Y-%m-%d %H:%M:%S")] = [duration]
            window_counter += 1
            event_time += timedelta(minutes=1)

    # Calculate the average duration for each time window
    average_duration_dict = {}
    for timestamp, durations in events_by_time.items():
        average_duration = sum(durations) / len(durations)
        average_duration_dict[timestamp] = average_duration

    return average_duration_dict

def main():

    try:
        # Parse command-line arguments
        args = parse_args()

        # Open the input JSON file and load its data
        with open(args.input_file, 'r') as file:
            events = [json.loads(line) for line in file]

        # Sort events by timestamp
        events.sort(key=lambda x: x['timestamp'])

        # Calculate moving average and get the output
        output = calculate_moving_average(events, args.window_size)

        # Print the results in the desired format
        for timestamp, avg_duration in output.items():
            print(json.dumps({
                "date": timestamp,
                "average_delivery_time": avg_duration
            }))

        # Write output to output.json with each event on a separate line
        with open('output.json', 'w') as output_file:
            json.dump(output, output_file)
    
    # Handle incorrectly typed files or unexisting ones
    except FileNotFoundError:
        print(f"The file '{args.input_file}' was not found.")

if __name__ == "__main__":
    main()
