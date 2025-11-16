import re

def is_arabic_word(word):
    return re.fullmatch(r'[\u0600-\u06FF]+', word)

def is_eligible_for_print(word):
    # تجاهل الكلمات التي تحتوي على 3 أحرف أو أكثر بدون ضبط
    return not re.fullmatch(r'[\u0600-\u065F]{1,3}', word)

def has_sufficient_diacritics(word):
    # تجاهل الكلمات التي لا تحتوي على حركات أو تحتوي على حرف واحد فقط مشكول
    return re.search(r'[\u064B-\u0652]', word) and len(re.findall(r'[\u0600-\u065F]', word)) > 2

def find_repeated_words(line):
    words = line.split()
    for i in range(len(words) - 1):
        if is_arabic_word(words[i]) and words[i] == words[i + 1] and is_eligible_for_print(words[i]) and has_sufficient_diacritics(words[i]):
            return words[i], words[i + 1]
    return None

def find_record_start(lines, current_index):
    start_pattern = r'\w{3,4}[،"]\ .*\،\ .*$'
    for i in range(current_index, -1, -1):
        if re.match(start_pattern, lines[i]):
            return lines[i]
    return "رأس السجل غير موجود"

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("-------------------------كلمات مكررة متجاورة--------------------------\n\n")
        for index, line in enumerate(lines):
            result = find_repeated_words(line)
            if result:
                record_start = find_record_start(lines, index)
                out_file.write(f'{record_start}{result[0]} {result[1]}: السياق/ الجملة الذي ورد فيها التكرار: {line}\n')

# استخدم اسم الملف الذي تريد معالجته واسم الملف الناتج
process_file('جذاذة.txt', 'تكرار الكلمة.txt')
