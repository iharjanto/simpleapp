import csv
import json
from django.core.serializers.json import DjangoJSONEncoder
import argparse


def csv_to_fixture(csv_file, model_name, output_file):
    """
    Convert CSV to Django fixture JSON format

    Args:
        csv_file (str): Path to input CSV file
        model_name (str): Django model name in format 'app.Model'
        output_file (str): Path to output JSON file
    """
    fixture_data = []

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for pk, row in enumerate(reader, start=1):
            fixture_data.append(
                {
                    "model": model_name,
                    "pk": pk,  # Auto-incrementing PK or use your own ID field
                    "fields": {
                        key: value
                        for key, value in row.items()
                        if key.lower() != "id"  # Exclude ID field if present
                    },
                }
            )

    with open(output_file, "w") as f:
        json.dump(fixture_data, f, indent=2, cls=DjangoJSONEncoder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mengubah json menjadi csv")
    parser.add_argument("-i", "--input", help="masukkan nama fileinput ")
    parser.add_argument(
        "-o", "--output", help="masukkan nama output file ", default="out.csv"
    )
    args = parser.parse_args()

    # Example Usage
    csv_to_fixture(
        csv_file=args.input, model_name="kurikulum.matakuliah", output_file=args.output
    )
