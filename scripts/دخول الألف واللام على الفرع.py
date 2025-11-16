import re

def find_three_words_pattern(input_file):
    pattern = r'^\w{3,4}\،\ .*\،\ .*$'
    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read().split('تاريخ آخر تحديث')

    for record in data:
        lines = record.split('\n')
        for line in lines:
            match = re.search(pattern, line.strip())
            if match:
                words = line.strip().split('،')
                if len(words) == 3 and words[1].strip().startswith('ال'):
                    results.append(line.strip())

    return results

three_words_results = find_three_words_pattern("جذاذة.txt")

# فتح الملف للكتابة وإضافة الجملة في البداية
with open("دخول الألف واللام على الفرع.txt", 'w', encoding='utf-8') as f:
    f.write("-------------------------حذف الألف واللام من الفرع--------------------------\n\n")
    f.write('\n'.join(three_words_results))
