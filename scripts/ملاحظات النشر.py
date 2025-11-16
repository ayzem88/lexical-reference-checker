

import re

def check_subsequent_line(record):
    lines_to_check = [
"التاريخ: تاريخ استعمال الشّاهد، مرتبط بـ",
"التاريخ: تاريخ استعمال الشاهد، مرتبط بـ",
"التاريخ: تاريخ استعمال الآية، مرتبط بـ",
"التعريف: التّعريفُ مُقتَبس من:",
"التعريف: التعريف مقتبس من:",
"التعريف: \"للمصطلح تعريفات تختلف باختلاف المذاهب",
"التوثيق: لم يَرِد الشّاهد في ديوان",
"التوثيق: لم يرد الشاهد في ديوان",
"التوثيق: لم يَرِد الشّاهد في كتاب",
"التوثيق: لم يرد الشاهد في كتاب",
"الشاهد: في المصدر",
"وسم اللفظ: يحتمل لفظُ",
"وسم اللفظ: يحتمل لفظ",
"الشاهد: ورد اللفظ في سياق غير استعمالي أسبق بتاريخ",
"الشاهد: ورد اللّفظ في سياق غير استعماليّ أسبق بتاريخ",
"الشاهد: \"الغالب أن الشاهد من عصر الاحتجاج، لكنه مجهول المستعمل والتاريخ",
"اللفظ: في المصدر:",
"اللفظ: ورد اللفظ بصور مختلفة",
"اللفظ: ورد اللّفظ بصُور مختلفة",
"المستعمل: ونُسِبَ إلى",
"المستعمل: ونسب إلى"

    ]

    first_line_pattern = find_first_line_pattern(record)
    lines_in_record = record.split("\n")

    for i, line in enumerate(lines_in_record):
        if "ملاحظات للنشر:" in line:
            if i+1 < len(lines_in_record) and not any(lines_in_record[i+1].startswith(line_to_check) for line_to_check in lines_to_check):
                return lines_in_record[i+1], first_line_pattern
    return None, None

def find_first_line_pattern(record):
    pattern = r'^\w{3,4}\،\ .*\،\ .*$'
    lines_in_record = record.split("\n")
    for line in lines_in_record:
        if re.match(pattern, line):
            return line
    return None

def save_results_to_file(filename, matching_patterns):
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write("-------------------------ملاحظات النشر غير المنمطة-------------------------\n\n")
        for pattern, first_line in matching_patterns:
            output_file.write(pattern + "\n")
            output_file.write(first_line + "\n")
            output_file.write("\n")

if __name__ == "__main__":
    with open("جذاذة.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    records = content.split("تاريخ آخر تحديث")

    matching_patterns = []

    for record in records:
        pattern, first_line = check_subsequent_line(record)
        if pattern and first_line:
            matching_patterns.append((first_line, pattern))

    save_results_to_file("ملاحظات النشر غير المنمطة.txt", matching_patterns)
