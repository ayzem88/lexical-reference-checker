import re

def extract_text(file_path):
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content into records
    records = content.split("تاريخ آخر تحديث")

    start_pattern = re.compile(r'ن?\d{1,4}هـ/\d{1,4}م|ن?\d{1,4}ق\.هـ/\d{1,4}م')
    end_pattern = re.compile(r'.*\(ت، \d{2,4}هـ\)|^.*،\ ط\d{1,9}،|^.*تحقيق|مراجعة|تقديم|ترجمة|تح|حواشيه|نشرها|نشره|رواية|ديوان|شعر:.*')
    exclude_patterns = [r'بطاطا']

    results = []

    for record in records:
        start = start_pattern.search(record)
        if start:
            end = end_pattern.search(record, start.end())
            if end:
                # Extract the text between the patterns, excluding certain lines
                text = record[start.end():end.start()].split('\n')
                # Exclude the line before the end pattern and the line containing the end pattern
                text = text[:-2]
                filtered_text = [line for line in text if not any(re.match(ep, line) for ep in exclude_patterns)]
                results.append('\n'.join(filtered_text))

    # Exclude the entire line that matches the start pattern and the line before the end pattern
    filtered_results = []
    for result in results:
        lines = result.split('\n')
        filtered_lines = [line for line in lines if not start_pattern.match(line)]
        filtered_results.append('\n'.join(filtered_lines))

    # Write the results to a new file
    with open('مراجعة الشواهد.txt', 'w', encoding='utf-8') as result_file:
        for result in filtered_results:
            result_file.write(result + "\n\n---\n\n")

# Use the function with the correct file path
extract_text('جذاذة.txt')
