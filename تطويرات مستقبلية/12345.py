import re

# Arabic diacritics
diacritics = "ًٌٍَُِّْ"

# Patterns
start_pattern = r'^تاريخ آخر تحديث:'
end_keyword = 'تاريخ آخر تحديث:'
date_pattern = r'^ن?\d{1,4}ق\.هـ/\d{1,4}م|^ن?\d{1,4}هـ/\d{1,4}م'
al_definite_pattern = r'\bالَ|الِ|الُ'

# Input and output file paths
input_file_path = 'جذاذة.txt'
output_file_path = 'أل التعريف.txt'

# Read the file
with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Split into records based on "تاريخ آخر تحديث"
records = re.split(start_pattern, content)

# Process each record
results = []
for record in records:
    if end_keyword in record:
        # Find words with أل التعريف with incorrect diacritics
        matches = re.findall(r'\b(\S*?(الَ|الِ|الُ)\S*?)\b', record)
        for match in matches:
            word = match[0]
            # Append the incorrect word and the corresponding record
            results.append(f'# {word}')
            results.append(record.strip())
            results.append('')  # Add a blank line for separation

# Write the results to the output file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write('\n'.join(results))

print(f'Results have been saved to {output_file_path}')
