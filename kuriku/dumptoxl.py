import json
import pandas as pd
from collections import defaultdict
from openpyxl import Workbook
import re


def django_json_to_excel(input_json, output_excel):
    """
    Convert Django dumpdata JSON to Excel with each model in separate sheet

    Args:
        input_json (str): Path to input JSON file
        output_excel (str): Path to output Excel file (.xlsx)
    """
    # Load JSON data
    with open(input_json, "r") as f:
        data = json.load(f)

    # Group records by model
    model_data = defaultdict(list)
    for item in data:
        model_data[item["model"]].append(item)

    # Create Excel writer
    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        for model, items in model_data.items():
            # Process records for this model
            records = []
            for item in items:
                record = {"id": item["pk"]}
                # Handle fields and relationships
                for field, value in item["fields"].items():
                    if isinstance(value, dict) and "pk" in value:  # ForeignKey
                        record[f"{field}_id"] = value["pk"]
                    elif isinstance(value, list):  # ManyToMany
                        record[field] = ",".join(str(v["pk"]) for v in value)
                    else:
                        record[field] = value
                records.append(record)

            # Create clean sheet name
            app_label, model_name = model.split(".")
            sheet_name = f"{app_label}_{model_name}"[:31]  # Excel sheet name limit

            # Remove invalid characters from sheet name
            sheet_name = re.sub(r"[\\/*?:[\]]", "", sheet_name)

            # Write to Excel sheet
            df = pd.DataFrame(records)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Successfully created {output_excel} with {len(model_data)} worksheets")


# Usage example
django_json_to_excel("kurikulum.json", "output.xlsx")
