import re

def extract_specific_records(input_file):
    # نمط البحث عن الخاصية الجديدة
    new_pattern = r'^\w{3,4}\،\ .*\،\ اسْمٌ مُصَغَّر$'
    
    # قائمة بالأنماط التي ترغب في التحقق منها
    specific_word_patterns = [
        r'[آءؤئأا-ي]َ[ا][آءؤئأا-ي]ّ',
        r'[آءؤئأا-ي][ُ]?[آءؤئأا-ي][َ]?[ي][ّ]?[ِ]?[آءؤئأا-ي]',
        r'[آءؤئأا-ي][ُ]?[آءؤئأا-ي][َ]?[ي][ّ]?[ِ]?[آءؤئأا-ي]',
        r'[آءؤئأا-ي][ُ]?[و][ّ]?[َ]?[ي][ْ]?[آءؤئأا-ي][ِ]?[آءؤئأا-ي]',
        r'[آءؤئأا-ي][ُ][آءؤئأا-ي][َ][ي][ْ][آءؤئأا-ي]',
        r'[آءؤئأا-ي][ُ][آءؤئأا-ي][َ][ي][ّ]',
        r'[آءؤئأا-ي][ُ][آءؤئأا-ي][َ][ي][ْ][آءؤئأا-ي][ِ][ي][آءؤئأا-ي]',
        r'[آءؤئأا-ي][ُ][و][َ][ي][ْ][آءؤئأا-ي][ِ][آءؤئأا-ي]',
        r'[آءؤئأا-ي][ُ][و][َ][ي][ْ][آءؤئأا-ي][ِ][ي][آءؤئأا-ي]',
        r'[آؤءئأا-ي][ُ]?[آؤءئأا-ي][َ]?[ن][ْ]?[آؤءئأا-ي][ِ]?[ي][َ]?ة',
        r'[آؤءئأا-ي][ُ]?[آؤءئأا-ي][ّ]?[َ]?[ي][ْ]?[آؤءئأا-ي][َ]?ة',
        r'[ا][آءؤئأا-ي][ْ][آءؤئأا-ي][ِ][آءؤئأا-ي][ّ][َ][ا][آءؤئأا-ي]',
        r'[ا][آءؤئأا-ي][ْ][آءؤئأا-ي][ِ][ن][ْ][آءؤئأا-ي][َ][ا][آءؤئأا-ي]'

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
intro_sentence = "-------------------------مراجعة وسم الاسم المصغر---------------------------"

# حفظ النتائج في ملف جديد
with open("خطأ في وسم الاسم المصغر.txt", 'w', encoding='utf-8') as f:
    f.write(intro_sentence + '\n\n')
    f.write('\n'.join(specific_records))
