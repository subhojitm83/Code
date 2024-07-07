import pandas as pd
import numpy as np
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_file(input_file_path):
    logging.info(f"Reading data from {input_file_path}")
    data = pd.read_csv(input_file_path)
    logging.info("Data read successfully")
    return data

def get_avg_latency(input_file_path, output_file_path):
    logging.info("Starting the process to get average latency")

    data = read_file(input_file_path)
    logging.info("Filtering data where responseCode is 200")
    filtered_data = data[data['responseCode'] == 200]

    logging.info("Calculating average latency and 90th percentile latency")
    result = filtered_data.groupby('label').agg(
        avgLatency=('Latency', 'mean'),
        percentile90=('Latency', lambda x: np.percentile(x, 90))
    ).reset_index()

    result.columns = ['label', 'avgLatency', 'ninperlatency']

    logging.info(f"Saving the result to {output_file_path}")
    result.to_csv(output_file_path, index=False)
    logging.info("Result saved successfully")

if __name__ == '__main__':
    # Create the parser
    argument_parser = argparse.ArgumentParser(description='Response time generator')

    # Add the arguments
    argument_parser.add_argument('input_file_path', type=str, help='The path of the input CSV file')
    argument_parser.add_argument('output_file_path', type=str, help='The path of the output CSV file')

    # Execute the parse_args() method
    args = argument_parser.parse_args()

    logging.info("Script started")
    get_avg_latency(args.input_file_path, args.output_file_path)
    logging.info("Script finished")
