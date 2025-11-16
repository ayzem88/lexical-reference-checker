import re

def extract_matched_records(input_file):
    # أنماط البحث
    pattern1 = r'^\w{3,4}\،\ .*\،\ مُتَعَدٍّ بِالحَرْف$'
    pattern2 = r'^\w{3,4}\،\ .*\،\ مُتَعَدٍّ$'

    results = []
    matches1 = set()
    matches2 = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        records = f.read().split('تاريخ آخر تحديث')

    # البحث عن الأنماط في كل السجلات
    for record in records:
        lines = record.split('\n')
        for line in lines:
            if re.search(pattern1, line):
                matches1.add(line)
            elif re.search(pattern2, line):
                matches2.add(line)

    # عقد المقارنة بين الأنماط
    for match1 in matches1:
        word1 = match1.split('،')[1].strip()
        for match2 in matches2:
            word2 = match2.split('،')[1].strip()
            if word1 == word2 and (match1, match2) not in results:
                # إضافة السطرين فقط إذا كانت الكلمات متطابقة ولم يتم إضافتهما من قبل
                results.append((match1, match2))

    return results

# تنفيذ الوظيفة
matched_records = extract_matched_records("جذاذة.txt")
intro_sentence = "---جاء في الدليل: (‌ج. يُوسَم الفعلُ، بالنّظر إلى أصله النّحويّ ... 3. متعدٍّ بالحرف، بشرط أن يكون أصل الفعل غير متعدٍّ بنفسه ...---\n" + \
 "---راجع المتعدي بالحرف؛ بسبب مطابقته للمتعدي في الفرع، وهنا يشترط اختلاف المعنى أو حذف جذاذة المتعدي بالحرف---\n"
# حفظ النتائج في ملف جديد
with open("المتعدي بالحرف مع المتعدي.txt", 'w', encoding='utf-8') as f:
    f.write(intro_sentence + '\n')
    for match1, match2 in matched_records:
        f.write(match1 + '\n' + match2 + '\n\n')
