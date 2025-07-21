import json
import pandas as pd

def json_to_excel(json_file, output_file):
    # Open and load the JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Create a Pandas Excel writer object to write to Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Loop through each model data in the JSON file
        for entry in data:
            model_label = entry['model']  # e.g., "kurikulum.matakuliah"
            model_name = model_label.split('.')[-1].lower()  # Extract model name for the sheet name

            # Extract the 'fields' data (which contains the actual record data)
            fields_data = entry['fields']

            # Convert the data (list of records) into a pandas DataFrame
            df = pd.DataFrame([fields_data])

            # Write the model data to a separate sheet in the Excel file
            df.to_excel(writer, sheet_name=model_name, index=False)

            print(f"Data for model '{model_name}' written to '{model_name}' sheet")

    print(f"Excel file saved as '{output_file}'")

# Example usage
json_file = 'kurikulumdata.json'  # The Django dumpdata JSON file
output_file = 'dumped_data_template.xlsx'  # Output Excel file

json_to_excel(json_file, output_file)
