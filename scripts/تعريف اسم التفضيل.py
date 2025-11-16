import re

def extract_specific_records(input_file):
    # نمط البحث عن الخاصية الجديدة
    new_pattern = r'^\w{3,4}\،\ .*\،\ اسْمُ تَفْضِيل$'
    
    # نمط البحث عن التاريخ
    pattern1_with_q = r'^ن?\d{1,4}ق\.هـ/\d{1,4}م'
    pattern1_without_q = r'^ن?\d{1,4}هـ/\d{1,4}م'
        
    # نماط البحث بعد (:) مباشرة
    patterns_after_colon = [
        r'ال[أ][َ][ا-ي][ْ][ا-ي][َ][ا-ي][ُ]',
        r'ال[أ][َ][ا-ي][َ][ا-ي][ّ][ُ]',
        r'ال[أ][َ][ا-ي][ْ][ا-ي][َ][ى]'
    ]

    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        records = f.read().split('تاريخ آخر تحديث')

    for record in records:
        lines = record.split('\n')
        for i, line in enumerate(lines):
            if re.search(new_pattern, line):
                # إذا كان السطر التالي موجودًا
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    date_match_with_q = re.match(pattern1_with_q, next_line)
                    date_match_without_q = re.match(pattern1_without_q, next_line)
                    if date_match_with_q or date_match_without_q:
                        # التأكد من عدم وجود أي من النماط الثلاثة بعد (:) مباشرة
                        if not any(re.search(pattern, next_line) for pattern in patterns_after_colon):
                            results.append(line)
                            results.append(next_line)

    return results

specific_records = extract_specific_records("جذاذة.txt")

# العبارة التي سيتم إضافتها في بداية الملف
header = "-------------------------مراجعة تعريف اسم التفضيل------------------------\n\n"

# حفظ النتائج في ملف جديد مع إضافة العبارة في البداية
with open("خطأ في تعريف اسم التفضيل.txt", 'w', encoding='utf-8') as f:
    f.write(header)  # كتابة العبارة في أول الملف
    f.write('\n'.join(specific_records))  # كتابة النتائج بعد العبارة
