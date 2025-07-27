import pandas as pd
import argparse
import json


def json_to_csv_pandas(input_file, output_file):
    # Read JSON file

    # Load the JSON data
    with open(input_file, "r") as f:
        data = json.load(f)

    # Normalize the data - extract fields and pk separately
    df = pd.json_normalize(data, sep="_")

    # Create a new DataFrame with the structure we want
    processed_data = []
    for _, row in df.iterrows():
        record = {"pk": row["pk"]}
        record.update(row["fields"])
        processed_data.append(record)

    # Convert to DataFrame
    result_df = pd.DataFrame(processed_data)

    # Save to CSV
    result_df.to_csv(output_file, index=False)

    print("Conversion completed. Data saved to output.csv")


# Usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mengubah json menjadi csv")
    parser.add_argument("-i", "--input", help="masukkan nama fileinput ")
    parser.add_argument(
        "-o", "--output", help="masukkan nama output file ", default="out.csv"
    )
    args = parser.parse_args()
    json_to_csv_pandas(args.input, args.output)
