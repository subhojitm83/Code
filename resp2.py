import pandas as pd
import numpy as np
import argparse

def read_file(input_file_path):
    data = pd.read_csv(input_file_path)
    return data 

def get_avg_latency(input_file_path,output_file_path):
    data = read_file(input_file_path)
    filtered_data = data[data['responseCode'] == 200]


    result = filtered_data.groupby('label').agg(
        avgLatency=('Latency', 'mean'),
        percentile90=('Latency', lambda x: np.percentile(x, 90))
    ).reset_index()

    result.columns = ['label', 'avgLatency', 'ninperlatency']

    # Save the result to a new CSV file
    result.to_csv(output_file_path, index=False)

if __name__ == '__main__':
    # Create the parser
    argument_parser = argparse.ArgumentParser(description='response time generator')

    # Add the arguments
    argument_parser.add_argument('input_file_path', type=str, help='The path of the csv file')
    argument_parser.add_argument('output_file_path', type=str, help='The path of the csv file')

    # Execute the parse_args() method
    args = argument_parser.parse_args()

    get_avg_latency(args.input_file_path, args.output_file_path)