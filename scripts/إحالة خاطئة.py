import re

# تعريف الثوابت للتعبيرات النمطية
HEADER_PATTERN = r'^\w{3,4}،\ .*،\ .*$'
IGNORE_PATTERN = r'\(.*\ \جَمع\ \لـ\:\ .*\)|\(.*\ \لُغة\ \في\:\ .*\)'
PATTERN1_WITH_Q = r'ن?\d{1,4}ق\.هـ/\d{1,4}م'
PATTERN1_WITHOUT_Q = r'ن?\d{1,4}هـ/\d{1,4}م'
PATTERN_H = r'الإحالة:'

# تعريف مجموعة الأحرف العربية وعلامات التشكيل
ARABIC_LETTERS = '\u0621-\u063A\u0641-\u064A'
ARABIC_DIACRITICS = '\u064B-\u0652'
ARABIC_CHARS = ARABIC_LETTERS + ARABIC_DIACRITICS

def extract_root_from_section(section):
    """
    استخراج الجذر من القسم.
    """
    for line in section.split("\n"):
        if re.match(HEADER_PATTERN, line):
            return line.split('،')[0].strip()
    return ''

def search_pattern_with_reference(section, output_file):
    """
    البحث عن الجذور التي لا تظهر بعد الشارحة ولكن تحتوي على 'الإحالة:'.
    """
    root = extract_root_from_section(section)
    if not root or len(root) < 3:
        return

    # تعريف نمط الكلمة للجذر باستخدام الأحرف العربية وعلامات التشكيل
    word_pattern = f'[{ARABIC_CHARS}]*{root[0]}[{ARABIC_DIACRITICS}]*[{ARABIC_CHARS}]*{root[1]}[{ARABIC_DIACRITICS}]*[{ARABIC_CHARS}]*{root[2]}[{ARABIC_DIACRITICS}]*[{ARABIC_CHARS}]*'

    root_found_after_colon = False

    for line in section.split("\n"):
        filtered_line = re.sub(IGNORE_PATTERN, '', line)
        if re.match(PATTERN1_WITH_Q, filtered_line) or re.match(PATTERN1_WITHOUT_Q, filtered_line):
            # تقسيم السطر عند الشارحة
            parts = filtered_line.split(':', 1)
            if len(parts) > 1:
                after_colon = parts[1]  # النص بعد الشارحة
                matches = re.finditer(word_pattern, after_colon)
                match_count = sum(1 for _ in matches)
                if match_count >= 1:
                    root_found_after_colon = True
                    break  # الجذر موجود بعد الشارحة
            else:
                # لا توجد شارحة في السطر، نعتبر أن الجذر غير موجود بعد الشارحة
                continue

    # إذا لم يتم العثور على الجذر بعد الشارحة، نتحقق من وجود 'الإحالة:'
    if not root_found_after_colon and re.search(PATTERN_H, section):
        for line in section.split("\n"):
            filtered_line = re.sub(IGNORE_PATTERN, '', line)
            if re.match(PATTERN1_WITH_Q, filtered_line) or re.match(PATTERN1_WITHOUT_Q, filtered_line):
                # طباعة السطر مع الإحالة
                reference_line = ''
                for sec_line in section.split("\n"):
                    if re.search(PATTERN_H, sec_line):
                        reference_line = sec_line.strip()
                        break
                output_file.write(filtered_line.strip() + " || " + reference_line + "\n\n")
                break  # لا نحتاج لمزيد من التحقق

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
            output_file.write("\n-------------------------إحالات خاطئة----------------------------------\n\n")
            for section in sections:
                search_pattern_with_reference(section, output_file)

    except IOError as e:
        print(f"حدث خطأ أثناء الكتابة إلى الملف: {e}")

def main():
    process_file("جذاذة.txt", "إحالات خاطئة.txt")

if __name__ == "__main__":
    main()
