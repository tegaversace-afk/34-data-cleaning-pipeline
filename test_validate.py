import csv
from validate import validate_rows

# Read the CSV file
with open("test_data.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames
    rows = list(reader)

# Run the validation function
issues = validate_rows(rows, headers)

# Display the results
print("VALIDATION RESULTS")
print("-" * 40)

for issue in issues:
    print(issue)

print("-" * 40)
print(f"Total records: {len(rows)}")
print(f"Total issues found: {len(issues)}")