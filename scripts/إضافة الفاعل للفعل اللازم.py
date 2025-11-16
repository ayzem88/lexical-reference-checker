import re

def extract_specific_records(input_file):
    # نمط البحث عن ثلاث كلمات وآخرها "لَازِم"
    laazim_pattern = r'^\w{3,4}\،\ .*\،\ لَازِم$'

    # نمط البحث عن التاريخ
    pattern1_with_q = r'^ن?\d{1,4}ق\.هـ/\d{1,4}م'
    pattern1_without_q = r'^ن?\d{1,4}هـ/\d{1,4}م'

    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        records = f.read().split('تاريخ آخر تحديث')

    for record in records:
        lines = record.split('\n')
        for i, line in enumerate(lines):
            if re.search(laazim_pattern, line):
                # إذا كان السطر التالي موجودًا
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    date_match_with_q = re.match(pattern1_with_q, next_line)
                    date_match_without_q = re.match(pattern1_without_q, next_line)
                    if date_match_with_q or date_match_without_q:
                        # الحصول على النص بين النمط والشارحة
                        content = next_line.split('،', 1)[1].split(':', 1)[0].strip()
                        # إذا كانت كلمة واحدة فقط
                        if len(content.split()) == 1:
                            results.append(line)
                            results.append(next_line)

    return results

# تنفيذ الوظيفة
specific_records = extract_specific_records("جذاذة.txt")
intro_sentence = "------------------------------رأس التعريف بحاجة إلى فاعل------------------------------"

# حفظ النتائج في ملف جديد
with open("إضافة الفاعل للفعل اللازم.txt", 'w', encoding='utf-8') as f:
    f.write(intro_sentence + '\n\n')
    f.write('\n'.join(specific_records))
