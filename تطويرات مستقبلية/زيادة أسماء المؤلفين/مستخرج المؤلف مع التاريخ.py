import re

def extract_patterns(file_path):
    # نمط البحث للتاريخ والنمط الذي يسبقه
    date_pattern = r'ن?\d{1,4}هـ/\d{1,4}م|ن?\d{1,4}ق\.هـ/\d{1,4}م'
    preceding_line_pattern = r'.*\(ت، \d{2,4}هـ\)|^.*،\ ط\d{1,9}،|^.*تحقيق|مراجعة|تقديم|ترجمة|تح|حواشيه|نشرها|نشره|رواية|ديوان|شعر:.*'
    
    results = []

    with open(file_path, 'r', encoding='utf-8') as file:
        # قراءة السجلات بين "تاريخ آخر تحديث" والبداية
        records = re.split(r'تاريخ آخر تحديث', file.read())

        for record in records:
            # البحث عن التواريخ في السجل
            dates = re.findall(date_pattern, record)

            # تقسيم السجل إلى أسطر للبحث عن النمط السابق للتاريخ
            lines = record.split('\n')
            for date in dates:
                for i in range(len(lines)):
                    if re.search(preceding_line_pattern, lines[i]):
                        # إضافة التاريخ والسطر الذي يسبق النمط
                        results.append((date, lines[i-1]))
                        break

    # كتابة النتائج في ملف جديد
    with open('نتائج.txt', 'w', encoding='utf-8') as output_file:
        for date, line in results:
            output_file.write(f'{date} = {line}\n')

    return 'تمت العملية بنجاح.'

# يتم استدعاء الدالة هنا مع المسار المحدد للملف
extract_patterns("1.txt")
