import re

# تعريف الثوابت للتعبيرات النمطية
HEADER_PATTERN = r'^\w{3,4}،\ .*،\ .*$'
IGNORE_PATTERN = r'\(.*\ \جَمع\ \لـ\:\ .*\)|\(.*\ \لُغة\ \في\:\ .*\)'
PATTERN1_WITH_Q = r'ن?\d{1,4}ق\.هـ/\d{1,4}م'
PATTERN1_WITHOUT_Q = r'ن?\d{1,4}هـ/\d{1,4}م'
PATTERN_H = r'الإحالة:'

def extract_root_from_section(section):
    """
    استخراج الجذر من القسم.
    """
    for line in section.split("\n"):
        if re.match(HEADER_PATTERN, line):
            return line.split('،')[0].strip()
    return ''

def search_pattern_in_section(section, output_file):
    """
    البحث عن نمط في القسم وكتابة النتائج في ملف.
    """
    root = extract_root_from_section(section)
    if not root:
        return

    # التحقق من وجود عبارة 'الإحالة:' في القسم
    if re.search(PATTERN_H, section):
        return

    #word_pattern = rf'\b[\w]*[{root[0]}][ًٌٍَُِّْ]?[\w]*[{root[1]}][ًٌٍَُِّْ]?[\w]*[{root[2]}][ًٌٍَُِّْ]?[\w]*\b' #هذا يسمح بوجود حركة أو عدم وجودها، لكن ليس اكثر من حركة للحرف
    word_pattern = rf'\b[\w]*[{root[0]}][ًٌٍَُِّْ]*[\w]*[{root[1]}][ًٌٍَُِّْ]*[\w]*[{root[2]}][ًٌٍَُِّْ]*[\w]*\b'

    for line in section.split("\n"):
        filtered_line = re.sub(IGNORE_PATTERN, '', line)  # تجاهل الأجزاء المطابقة للنمط

        if re.match(PATTERN1_WITH_Q, filtered_line) or re.match(PATTERN1_WITHOUT_Q, filtered_line):
            matches = re.finditer(word_pattern, filtered_line)
            match_count = sum(1 for _ in matches)

            if match_count >= 2:
                output_file.write(filtered_line.strip() + "\n\n")

def read_file_content(input_file_path):
    """
    قراءة محتوى الملف.
    """
    try:
        with open(input_file_path, encoding="utf8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"لم يتم العثور على الملف: {input_file_path}")
        return None

def process_file(input_file_path, output_file_path):
    """
    معالجة الملف: قراءة البيانات وكتابة النتائج في ملف آخر.
    """
    content = read_file_content(input_file_path)
    if content is None:
        return

    sections = content.split("تاريخ آخر تحديث")

    try:
        with open(output_file_path, "w", encoding="utf8") as output_file:
            output_file.write("-------------------------هذه جذاذات دون إحالة----------------------------------\n\n")
            for section in sections:
                search_pattern_in_section(section, output_file)
    except IOError as e:
        print(f"حدث خطأ أثناء الكتابة إلى الملف: {e}")

def main():
    process_file("جذاذة.txt", "جذاذات دون إحالة.txt")

if __name__ == "__main__":
    main()
