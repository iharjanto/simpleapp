import argparse
import pandas as pd
import json

def xl_to_json(excel_file, output_json_file, app_name):
    # Read the Excel file
    xl = pd.ExcelFile(excel_file)
    
    # List to store all models' data
    all_data = []

    # Loop through each sheet in the Excel file
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)  # Read the sheet into a DataFrame
        
        model_name = sheet_name  # Sheet name corresponds to the model name
        model_label = f"{app_name}.{model_name}"  # Full model name (e.g., app_name.model_name)
        
        # Iterate over each row in the DataFrame to create model instances
        for index, row in df.iterrows():
            # Prepare the data for each instance (adding pk and fields)
            record = {
                "model": model_label,
                "pk": index + 1,  # Set pk based on row index or custom logic
                "fields": row.to_dict()  # Use row values as fields
            }
            all_data.append(record)

    # Write all the collected data to a JSON file
    with open(output_json_file, 'w') as json_file:
        json.dump(all_data, json_file, indent=4)

    print(f"Excel data has been converted to JSON and saved to {output_json_file}")

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Convert Excel file to Django dumpdata JSON format.")
    
    # Add arguments
    parser.add_argument('excel_file', help="Path to the Excel file to convert")
    parser.add_argument('output_json_file', help="Path to the output JSON file")
    parser.add_argument('app_name', help="Django app name to prefix the model names (e.g., 'kurikulum')")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the conversion function with parsed arguments
    xl_to_json(args.excel_file, args.output_json_file, args.app_name)

if __name__ == '__main__':
    main()
