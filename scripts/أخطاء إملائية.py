import re

class FileManager:
    """مسؤول عن قراءة وكتابة الملفات."""
    @staticmethod
    def read_file(path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def write_file(path, content):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)


class HarakatChecker:
    """دوال مساعدة لفحص الحركات والتشكيل."""
    diacritics = "ًٌٍَُِّْ"
    harakat_range = '\u064B-\u0652'

    @staticmethod
    def has_invalid_repeated_harakat(word):
        pattern = r'([' + HarakatChecker.harakat_range + r'])\1'
        return bool(re.search(pattern, word))

    @staticmethod
    def find_repeated_harakat(record):
        error_words = set()
        for line in record.split("\n"):
            for word in line.split():
                if HarakatChecker.has_invalid_repeated_harakat(word):
                    error_words.add(word)
        return error_words


def extract_words_with_filter_and_header(
    input_file, output_file, target_letters, start_pattern, end_keyword, date_pattern, allowed_start_words
):
    """استخراج الكلمات مع التصفية والعناوين."""
    start_pattern_regex = re.compile(start_pattern, re.MULTILINE)
    date_pattern_regex = re.compile(date_pattern)
    allowed_start_words_regex = re.compile(rf'^({"|".join(allowed_start_words)})')
    filter_pattern = re.compile(r"^(لُغة|جَمع|في|\(|\[.*\])")
    diacritics = HarakatChecker.diacritics

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        records = content.split(end_keyword)

    results = []
    for record in records:
        header_match = start_pattern_regex.search(record)
        header = header_match.group(0) if header_match else "Header Not Found"
        lines = record.strip().split('\n')
        for line in lines:
            if (line.startswith('"') and line.endswith('"') or 
                date_pattern_regex.match(line) or 
                allowed_start_words_regex.match(line)):
                text_to_check = re.split(date_pattern_regex, line)[-1] if date_pattern_regex.match(line) else line
                words = text_to_check.split()
                for word in words:
                    has_error = False
                    for idx, letter in enumerate(word):
                        if letter in target_letters:
                            # Check if the letter has a diacritic immediately after it
                            if idx+1 < len(word) and word[idx+1] in diacritics:
                                continue
                            else:
                                has_error = True
                                break
                    if has_error:
                        results.append((header, word, line))
    
    # كتابة النتائج في ملف
    with open(output_file, 'w', encoding='utf-8') as out:
        for header, word, line in results:
            out.write(f"{header} | {word} | {line}\n")


class TextProcessor:
    """معالجة النصوص واستخراج السجلات والأخطاء."""
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.records = []

    def split_records(self, content):
        return content.split("تاريخ آخر تحديث")

    def extract_text(self):
        content = FileManager.read_file(self.input_file_path)
        records = self.split_records(content)
        start_pattern = re.compile(r'ن?\d{1,4}هـ/\d{1,4}م|ن?\d{1,4}ق\.هـ/\d{1,4}م')
        end_pattern = re.compile(
            r'.*\(ت، \d{2,4}هـ\)|^.*،\ ط\d{1,9}،|^.*تحقيق|مراجعة|تقديم|ترجمة|تح|حواشيه|نشرها|نشره|رواية|ديوان|شعر:.*|https'
        )
        exclude_patterns = [r'\(.*\)']
        results = []

        for record in records:
            lines = record.strip().split('\n')
            for i, line in enumerate(lines):
                if start_pattern.search(line):
                    root_line = lines[i-1].strip() if i > 0 else ''
                    end = None
                    for j in range(i+1, len(lines)):
                        if end_pattern.search(lines[j]):
                            end = j
                            break
                    if end:
                        extracted_lines = lines[i:end]
                        if root_line:
                            extracted_lines.insert(0, root_line)
                        filtered_text = [
                            l for l in extracted_lines 
                            if not any(re.match(ep, l) for ep in exclude_patterns)
                        ]
                        results.append('\n'.join(filtered_text))
        
        # إزالة السطور التي تطابق نمط البداية
        filtered_results = []
        for result in results:
            lines = result.split('\n')
            filtered_lines = [line for line in lines if not start_pattern.match(line)]
            filtered_results.append('\n'.join(filtered_lines))
        
        self.records = filtered_results

    def process_records(self):
        diacritics = HarakatChecker.diacritics
        target_letters = [
            'ب','ت','ث','ج','ح','خ','د','ذ','ر','ز',
            'س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ك',
            'م','ن','ه','ء','ئ','ؤ', 'و', 'ي'
        ]
        sun_letters = set(['ت','ث','د','ذ','ر','ز','س','ش','ص','ض','ط','ظ','ل','ن'])
        moon_letters = set(['ا','ب','ج','ح','خ','ع','غ','ف','ق','ك','م','ه','و','ي','ء','ئ','ؤ','إ','آ','ة','ى','ـ'])
        
        def should_ignore_letter(word, index, letter):
            if letter == 'و':
                if index == 0:
                    return False
                return word[index - 1] == 'ُ'
            elif letter == 'ي':
                if index == 0:
                    return False
                return word[index - 1] == 'ِ'
            return False
        
        pattern_error_al = re.compile(r'^الْ[' + ''.join(moon_letters) + ']')
        words_to_search = [
            r'\bفِى\b', r'(?:\sعَلَي\s|\Aعَلَي\s|\sعَلَي\Z)',
            r'(?:\sعَلِى\s|\Aعَلِى\s|\sعَلِى\Z)', r'\bالَّذِى\b',
            r'\bالَّتِى\b', r'\b وَ \b', r'\b\w\َالا\w\ْ\b',
            r'\b\الا\w\ْ\b', r'عَبْدُال', r'عَبْدَال',
            r'\bأَىْ\b', r'\bأُمِّى\b', r'\bأَبِى\b',
            r'\bأَخِى\b', r'\bاَ\b', r'\bاِ\b',
            r'\bأُخْتِى\b', r'\bشَىْء\b', r'\bشَيْىء\b'
        ]
        pattern_to_search = re.compile('|'.join(words_to_search))
        saakin_pattern = re.compile(
            r'([\u0600-\u06FF]+ْ[\s\W]*ال[\u0600-\u06FF]+)'
        )
        
        output = ["-------------------------الأخطاء الإملائية----------------------------------\n\n"]
        
        for record in self.records:
            record = record.strip()
            if not record:
                continue
            
            lines = record.split('\n')
            if len(lines) < 3:
                continue
            
            erroneous_words = set()
            pattern_errors = set()
            saakin_errors = set()
            
            # تخطي أول وآخر سطر في السجل
            for line in lines[1:-1]:
                words = line.strip().split()
                for word in words:
                    clean_word = word.strip('،؛:؟!,.()[]{}"\'')
                    word_to_check = clean_word
                    has_missing_diacritic = False
                    
                    for index, letter in enumerate(word_to_check):
                        if letter in target_letters:
                            if letter == 'ا':
                                continue
                            elif letter in ['و', 'ي']:
                                if should_ignore_letter(word_to_check, index, letter):
                                    continue
                                else:
                                    if index + 1 >= len(word_to_check):
                                        has_missing_diacritic = True
                                        break
                                    next_char = word_to_check[index + 1]
                                    if next_char not in diacritics:
                                        has_missing_diacritic = True
                                        break
                            else:
                                if index + 1 >= len(word_to_check):
                                    has_missing_diacritic = True
                                    break
                                next_char = word_to_check[index + 1]
                                if next_char not in diacritics:
                                    has_missing_diacritic = True
                                    break
                    
                    if pattern_error_al.match(clean_word):
                        has_missing_diacritic = True
                    
                    if has_missing_diacritic:
                        erroneous_words.add(clean_word)
                    
                    if pattern_to_search.search(clean_word):
                        pattern_errors.add(clean_word)
                
                saakin_matches = saakin_pattern.findall(line)
                if saakin_matches:
                    saakin_errors.update(saakin_matches)
            
            repeated_harakat_errors = HarakatChecker.find_repeated_harakat(record)
            all_errors = erroneous_words.union(pattern_errors).union(saakin_errors).union(repeated_harakat_errors)
            
            if all_errors:
                error_list = '، '.join(sorted(all_errors))
                output.append(f"# {error_list}\n{record}\n\n")
        
        FileManager.write_file(self.output_file_path, ''.join(output))


def main():
    input_file_path = 'جذاذة.txt'
    output_file_path = 'الأخطاء الإملائية.txt'
    processor = TextProcessor(input_file_path, output_file_path)
    processor.extract_text()
    processor.process_records()


if __name__ == "__main__":
    main()
