import re

def extract_matching_lines(record):
    lines_in_record = record.split("\n")

    for index, line in enumerate(lines_in_record):
        # بحث عن الحالة الجديدة
        if "تَعَالَى" in line and "[" not in line and index > 0:
            # نطبع هذا السطر والسطر الذي قبله مباشرة
            return lines_in_record[index-1] + "\n" + line
    return None

def save_results_to_file(filename, matching_lines):
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write("---------------------------توثيق الآية القرآنية----------------------------\n\n")
        for line in matching_lines:
            output_file.write(line + "\n\n")

if __name__ == "__main__":
    with open("جذاذة.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    records = content.split("تاريخ آخر تحديث")

    matching_lines = []

    for record in records:
        result = extract_matching_lines(record)
        if result:
            matching_lines.append(result)

    save_results_to_file("توثيق الآية الداخلي.txt", matching_lines)
