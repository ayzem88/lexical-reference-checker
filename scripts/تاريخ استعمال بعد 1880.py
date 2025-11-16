import re

def find_pattern_case3(input_file):
    # النماذج المعدلة لتشمل الأربع حالات
    pattern1 = r'^(ن?\d{1,4}ق\.هـ/(\d{1,4})م)،'
    pattern2 = r'^(ن?\d{1,4}هـ/(\d{1,4})م)،'
    
    pattern3 = r'^التاريخ: تاريخ'

    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read().split('تاريخ آخر تحديث')

    for record in data:
        lines = record.split('\n')
        for index, line in enumerate(lines):
            match1 = re.search(pattern1, line)
            match2 = re.search(pattern2, line)
            
            # اختبار حالة قبل الهجرة مع النون أو دونها
            if match1 and int(match1.group(2)) > 1880:
                match = match1
            # اختبار حالة بعد الهجرة مع النون أو دونها
            elif match2 and int(match2.group(2)) > 1880:
                match = match2
            else:
                continue

            # بحث عن الشرط الثاني
            pattern3_found = any([re.search(pattern3, subsequent_line) for subsequent_line in lines[index+1:]])
            if not pattern3_found:
                if index > 0:  # للتأكد من وجود سطر قبل السطر الحالي
                    results.append(lines[index-1])
                results.append(line)
                intro_sentence = "-----------------مصادر حديثة، المرجح أنها تاريخ استعمال-------------------"

    with open("تاريخ استعمال بعد 1880.txt", 'w', encoding='utf-8') as f:
        f.write(intro_sentence + '\n\n')
        f.write('\n'.join(results))
    return results
case3_results = find_pattern_case3("جذاذة.txt")
