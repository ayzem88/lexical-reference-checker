import re

def find_pattern_case1(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read().split('تاريخ آخر تحديث')

    pattern1_with_q = r'^ن\d{1,4}ق\.هـ/\d{1,4}م'
    pattern1_without_q = r'^ن\d{1,4}هـ/\d{1,4}م'
    pattern2 = r'^التاريخ: تاريخ'

    results = []

    for record in data:
        lines = record.split('\n')
        for index, line in enumerate(lines):
            if re.search(pattern1_with_q, line) or re.search(pattern1_without_q, line):
                for subsequent_line in lines[index+1:]:
                    if re.search(pattern2, subsequent_line):
                        results.append(line)
                        break

    return results

def find_pattern_case2(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read().split('تاريخ آخر تحديث')

    pattern1_with_q = r'^\d{1,4}ق\.هـ/\d{1,4}م'
    pattern1_without_q = r'^\d{1,4}هـ/\d{1,4}م'
    pattern2 = r'التاريخ: تاريخ'

    results = []

    for record in data:
        lines = record.split('\n')
        for index, line in enumerate(lines):
            if re.search(pattern1_with_q, line) or re.search(pattern1_without_q, line):
                # بحث عن الشرط الثاني
                pattern2_found = any([re.search(pattern2, subsequent_line) for subsequent_line in lines[index+1:]])
                if not pattern2_found:
                    results.append(line)

    return results

# تنفيذ الوظائف
intro_sentence1 = "------------------------------لاحظ التقاء (ن) نحو مع ملاحظة تاريخ الاستعمال!------------------------------"
intro_sentence2 = "------------------------------لاحظ أنه تاريخ استعمال، ولكن دون ملاحظة نشر تسوّغه------------------------------"


case1_results = find_pattern_case1("جذاذة.txt")
case2_results = find_pattern_case2("جذاذة.txt")

with open("تاريخ استعمال.txt", 'w', encoding='utf-8') as f:
    f.write(intro_sentence1 + '\n\n')
    f.write('\n'.join(case1_results)+'\n')
    f.write(intro_sentence2 + '\n\n')
    f.write('\n'.join(case2_results))
