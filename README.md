# Translation Delivery Time CLI
This command-line application parses a stream of translation events and produces aggregated output by calculating a moving average of translation delivery time.

## Installation
To run the Translation Delivery Time CLI, you'll need Python 3.7.x or higher installed on your system.

1. Clone this repository;
2. Navigate to the project directory.

## Build
No build step is required as this is a Python script.

## Usage
Run the CLI with the following command:

```

python translation_delivery_time.py --input_file events.json --window_size 10

```

* '--input_file': Path to the input JSON file containing translation events.
* '--window_size': The size of the window for calculating the moving average.
  
The output will be printed to the console and also saved to 'output.json' in the same directory.

## Testing
To test the application, you can provide sample input files and verify if the output matches the expected results.

1. Prepare a test input file (e.g., test_events.json) with sample translation events.
2. Run the CLI with the test input file:

```

python translation_delivery_time.py --input_file test_events.json --window_size 5

```

3. Verify that the output matches the expected results.
   
## Input Format
The input file should be in JSON format, with each line representing a translation event. Each event should contain the following fields:

* timestamp: The timestamp of the event in the format YYYY-MM-DD HH:MM:SS.uuuuuu.
* translation_id: Unique identifier for the translation.
* source_language: Source language of the translation.
* target_language: Target language of the translation.
* client_name: Name of the client.
* event_name: Type of event.
* nr_words: Number of words in the translation.
* duration: Duration of the translation delivery.

Example input:

```json
{"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159", "translation_id": "5aa5b2f39f7254a75aa4", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb3", "source_language": "en", "target_language": "fr", "client_name": "taxi-eats", "event_name": "translation_delivered", "nr_words": 100, "duration": 54}
```
## Output Format
The output will be in JSON format, with each line representing a minute and its corresponding moving average delivery time.

Example output:

```json
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0.0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20.0}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31.0}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31.0}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

## Requirements
* Python 3.7.x or higher

## Additional Notes

Starting this project has been quite a rewarding experience, mixing my technical know-how with creative thinking to solve problems. It's been more than just a showcase of my technical abilities; it's been a chance to demonstrate my logical skills and how well I can handle tough problems.

One part of the project that really caught my interest was the need to think before you start coding to solve the problem. It pushed me to think carefully about how each event interacted with the desired output, making sure everything was accurate and efficient. Coming up with a solution that could handle tricky situations, do precise calculations, and still be easy for users to interact with was a challenge I took on eagerly and with a lot of attention to detail.
