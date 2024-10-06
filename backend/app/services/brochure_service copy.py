import re
import json

# Define the regular expression pattern to match quantity information
quantity_pattern = re.compile(
    r'(\b\d+(\.\d+)?\s*(x\s*\d*\s*(kg|g|ml|ltr|pk|ea|cm|mm)\b)?)'
    r'|(\b\d+\s*x\b)'
    r'|(\b\d+/\d+\b)'
    r'|(\(\s*av\s*\))',
    flags=re.IGNORECASE
)
def remove_quantities(data):
    """
    Recursively remove quantity information from product names in a nested data structure.
    """
    if isinstance(data, dict):
        return {key: remove_quantities(value) for key, value in data.items()}
    elif isinstance(data, list):
        cleaned_list = []
        for item in data:
            # Apply the regex substitution if the item is a string
            if isinstance(item, str):
                cleaned_item = quantity_pattern.sub('', item).strip()
                cleaned_list.append(cleaned_item)
            else:
                # Recursively process if the item is a list or dict
                cleaned_list.append(remove_quantities(item))
        return cleaned_list
    else:
        return data

# Load your JSON data from a file (replace 'data.json' with your actual file path)
with open('/Users/rohithkyla/FoodDist/backend/app/services/foodsBrochure.json', 'r') as f:
    data = json.load(f)

# Remove quantity information
clean_data = remove_quantities(data)

# Save the cleaned data to a new file (replace 'clean_data.json' with your desired output file)
with open('/Users/rohithkyla/FoodDist/backend/app/services/cBrochure.json', 'w') as f:
    json.dump(clean_data, f, indent=4)
