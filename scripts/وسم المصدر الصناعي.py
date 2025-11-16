import re

def extract_specific_records(input_file):
    # نمط البحث عن الخاصية الجديدة
    new_pattern = r'^\w{3,4}\،\ .+يّ\،\ مَصْدَرٌ صِنَاعِيّ$'
    
    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        records = f.read().split('تاريخ آخر تحديث')

    for record in records:
        lines = record.split('\n')
        
        for i, line in enumerate(lines):
            if re.search(new_pattern, line):
                # الحصول على النص بين الفاصلة الأولى والثانية
                extracted_word = line.split('،')[1].strip()
                results.append(line)

    return results

# تنفيذ الوظيفة
specific_records = extract_specific_records("جذاذة.txt")
intro_sentence = "-------------------------مراجعة وسم المصدر الصناعي------------------------\n\n"

# حفظ النتائج في ملف جديد
with open("خطأ في الوسم في المصدر الصناعي.txt", 'w', encoding='utf-8') as f:
    f.write(intro_sentence + '\n\n')
    f.write('\n'.join(specific_records))
