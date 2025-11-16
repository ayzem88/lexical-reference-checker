import re

def contains_case_4_pattern(record):
    # البحث عن نمط قال وكتب
    qala_matches = re.findall(r'^قَالَ (?![يَ])\w+.*$', record, re.M)
    katba_matches = re.findall(r'^كَتَبَ .*$', record, re.M)
    
    return qala_matches + katba_matches

if __name__ == "__main__":
    with open("جذاذة.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    records = content.split("تاريخ آخر تحديث")

    header_pattern = r'^\w{3,4}[،"]\ .*\،\ .*$'
    output_text = "----------------------------تعديل أول التقدمة-----------------------------\n\n"

    for record in records:
        header_match = re.search(header_pattern, record, re.M)
        if header_match:
            header_line = header_match.group()
            matching_lines = contains_case_4_pattern(record)
            if matching_lines:
                output_text += header_line + "\n"
                for line in matching_lines:
                    output_text += line + "\n"
                output_text += "\n"

    with open("قال ليس بعدها فعل مضارع.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(output_text)
