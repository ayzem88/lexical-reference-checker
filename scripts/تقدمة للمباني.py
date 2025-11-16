import re

def extract_new_case_lines(record):
    exclusion_pattern = r'^ن?\d{1,4}ق\.هـ/\d{1,4}م\،.*\((.*جَمع لـ:.*|.*لُغة في:.*)\)|^ن?\d{1,4}هـ/\d{1,4}م\،.*\((.*جَمع لـ:.*|.*لُغة في:.*)\)'
    main_pattern = r'(.*?(جَمع لـ|لُغة في).*?\n(قَالَ|قَالَت).*)'
    lines = record.split('\n')

    new_case_lines = []
    skip_next = False

    for i in range(len(lines) - 1):
        line = lines[i]

        if skip_next:
            skip_next = False
            continue

        if re.match(exclusion_pattern, line):
            skip_next = True
            continue

        if re.match(main_pattern, line + '\n' + lines[i + 1]):
            new_case_lines.append(line + '\n' + lines[i + 1])

    return new_case_lines

def save_results_to_file(filename, new_case_lines):
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write("-------------------------حذف التقدمة - جذاذة مبنى-------------------------\n\n")
        for line in new_case_lines:
            output_file.write(line + "\n\n")

if __name__ == "__main__":
    with open("جذاذة.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    records = content.split("تاريخ آخر تحديث")

    lines_new_case = []

    for record in records:
        lines_new_case.extend(extract_new_case_lines(record))

    save_results_to_file("تقدمة للمباني.txt", lines_new_case)
