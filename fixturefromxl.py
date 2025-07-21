import pandas as pd
import json

def excel_to_json_fixture(excel_file, model_name, app_name):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Prepare the list of dictionaries for the fixture
    fixture_data = []

    # Iterate through the rows of the dataframe and map them to Django model fields
    for index, row in df.iterrows():
        record = {
            "model": f"{app_name}.{model_name}",  # Format: app_name.model_name
            "pk": index + 1,  # Primary Key (adjust this if necessary)
            "fields": row.to_dict()  # Map the row to fields
        }
        fixture_data.append(record)

    # Write the fixture to a JSON file
    with open(f"{model_name}_fixture.json", "w") as json_file:
        json.dump(fixture_data, json_file, indent=4)

    print(f"Fixture data saved to {model_name}_fixture.json")

# Example usage
excel_file = 'matakuliah.xlsx'  # Your Excel file
model_name = 'matakuliah'       # Django model name (lowercase)
app_name = 'kurikulum'          # Django app name

excel_to_json_fixture(excel_file, model_name, app_name)
