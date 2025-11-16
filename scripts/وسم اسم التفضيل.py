import re

def extract_specific_records(input_file):
    # نمط البحث عن الخاصية الجديدة
    new_pattern = r'^\w{3,4}\،\ .*\،\ اسْمُ تَفْضِيل$'
    
    # قائمة بالأنماط التي ترغب في التحقق منها
    specific_word_patterns = [
                r'[أ][َ][ءؤئأا-ي][ْ][ءؤئأا-ي][َ][ءؤئأا-ي]',
                r'آ[آؤءئأا-ي][َ][آؤءئأا-ي]',
                r'آ[آؤءئأا-ي][َ]ى',
                r'[أ][َ][آؤءئأا-ي][َ][آؤءئأا-ي][ّ]',
                r'[إأؤءئآ-ي][ُ][آؤءئأا-ي][ْ][آؤءئأا-ي][َ][ى]',
                r'[أ][َ][آؤءئأا-ي][ّ][َ][آؤءئأا-ي]'
    ]

    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        records = f.read().split('تاريخ آخر تحديث')

    for record in records:
        lines = record.split('\n')
        matched = False  # flag to check if any pattern matched
        
        for i, line in enumerate(lines):
            if re.search(new_pattern, line):
                # الحصول على النص بين الفاصلة الأولى والثانية
                extracted_word = line.split('،')[1].strip()
                for pattern in specific_word_patterns:
                    if re.search(pattern, extracted_word):
                        matched = True
                        break
                if not matched:
                    results.append(line)

        if matched:
            continue

    return results

# تنفيذ الوظيفة
specific_records = extract_specific_records("جذاذة.txt")
intro_sentence = "-------------------------مراجعة وسم اسم التفضيل---------------------------"


# حفظ النتائج في ملف جديد
with open("خطأ في وسم اسم التفضيل.txt", 'w', encoding='utf-8') as f:
    f.write(intro_sentence + '\n\n')
    f.write('\n'.join(specific_records))
