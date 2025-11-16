import re

class TextProcessor:
    def __init__(self):
        self.arabic_diacritics_pattern = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED]')
        self.shadda_pattern = re.compile(r'\u0651')
        self.arabic_diacritic_pattern = r'[\u064B-\u065F\u0670\u06D6-\u06ED]'
        self.al_sun_letters = set('تثدذرزسشصضطظلن')
        self.root_and_date_pattern = re.compile(
            r'^(?P<pattern1>(?:[\wًٌٍَُِّْ]+(?:\s[\wًٌٍَُِّْ]+)?)\،\ .*\،\ '
            r'(?:(?:لَازِم|مُتَعَدٍّ|مُتَعَدٍّ بِالحَرْف|اسْم|مُلَازِمٌ لِلْبِنَاءِ لِلْمَجْهُول|'
            r'اسْمُ جَمْع|اسْمُ فِعْل|مَصْدَر|اسْمُ مَرَّة|مَصْدَرٌ مِيمِيّ|اسْمُ فَاعِل|'
            r'اسْمٌ مَنْسُوب|صِفَة|اسْمُ جِنْس|مَصْدَرٌ صِنَاعِيّ|اسْمُ مَفْعُول|فِعْلٌ نَاقِص|'
            r'صِيغَةُ مُبَالَغَة|اسْمُ صَوْت|اسْمُ هَيْئَة|ظَرْف|صِفَةٌ مُشَبَّهَة|'
            r'اسْمُ زَمَان|اسْمُ تَفْضِيل|مُثَنًّى عَلَى التَّغْلِيب|اسْمٌ مُصَغَّر|'
            r'اسْمُ آلَة|حَرْف|فِعْل|اسْمُ مَكَان)))$|'
            r'^(?P<pattern2>ن?\d{1,4}هـ/\d{1,4}م.*|ن?\d{1,4}ق\.هـ/\d{1,4}م.*)$',
            re.MULTILINE
        )
        self.arabic_letter_pattern = r'[\u0621-\u064A]'
        self.letter_with_diacritic_pattern = self.arabic_letter_pattern + self.arabic_diacritic_pattern + '*'

    def remove_diacritics(self, text):
        """Removes Arabic diacritics from the text."""
        return self.arabic_diacritics_pattern.sub('', text)

    def extract_root_and_date_lines(self, section):
        """Extracts the root and date lines from a section of text."""
        root_line = ''
        date_line = ''
        lines = section.strip().split('\n')
        for line in lines:
            match = self.root_and_date_pattern.match(line.strip())
            if match:
                if match.group('pattern1'):
                    root_line = line.strip()
                elif match.group('pattern2'):
                    date_line = line.strip()
                if root_line and date_line:
                    break
        return root_line, date_line

    def extract_word_before_colon(self, section):
        """Extracts the word before the colon in a section of text."""
        for line in section.split('\n'):
            if ':' in line:
                before_colon = line.split(':')[0]
                if '،' in before_colon:
                    after_comma = before_colon.split('،')[1]
                    words = after_comma.strip().split()
                    if words:
                        return words[0]
        return None

    def split_letters(self, word):
        """Splits a word into its letters, including diacritics."""
        return re.findall(self.letter_with_diacritic_pattern, word)

    def strip_definite_article(self, word):
        """Strips the Arabic definite article 'ال' من الكلمة."""
        match = re.match(r'^(ال)([\u064B-\u065F]*)', word)
        if match:
            return word[match.end():], True
        else:
            return word, False

    def compare_words(self, word1, word2):
        """Compares two Arabic words for diacritic differences on matching letters, ignoring specific cases."""
        word2_stripped, has_definite_article = self.strip_definite_article(word2)
        letters1 = self.split_letters(word1)
        letters2 = self.split_letters(word2_stripped)

        # تجاهل الحرف الأخير من الكلمة الثانية
        if len(letters2) > 1:
            letters2 = letters2[:-1]

        min_length = min(len(letters1), len(letters2))
        diacritics_diff = False

        for i in range(min_length):
            base_letter1 = self.remove_diacritics(letters1[i])
            base_letter2 = self.remove_diacritics(letters2[i])

            # تجاهل الحروف التي تختلف في الأساس
            if base_letter1 != base_letter2:
                continue

            # إذا كانت الكلمة تحتوي على "الـ" الشمسية وتكون الشدة على الحرف الأول
            if has_definite_article and i == 0 and base_letter2 in self.al_sun_letters:
                # تجاهل الشدة على الحرف الأول بعد "الـ"
                letter1_no_shadda = self.shadda_pattern.sub('', letters1[i])
                letter2_no_shadda = self.shadda_pattern.sub('', letters2[i])
                if letter1_no_shadda == letter2_no_shadda:
                    continue

            # تجاهل الاختلاف في التشكيل على الحرف الأخير من الكلمة الأولى إذا كان بدون تشكيل
            if i == len(letters1) - 1:
                if not re.search(self.arabic_diacritic_pattern, letters1[i]):
                    continue

            # إذا كانت التشكيلات مختلفة على نفس الحرف
            if letters1[i] != letters2[i]:
                diacritics_diff = True

        if diacritics_diff:
            return 'اختلاف في التشكيل'
        else:
            return 'تطابق كامل'

    def map_comparison_result(self, comparison_result):
        """Maps the comparison result to a readable message."""
        mapping = {
            'تطابق كامل': '[متطابق]',
            'اختلاف في التشكيل': '[اختلاف تشكيل]'
        }
        return mapping.get(comparison_result, '')

    def process_section(self, section, output_file):
        """Processes a section of text and writes the comparison result if هناك اختلاف."""
        root_line, date_line = self.extract_root_and_date_lines(section)
        if not root_line:
            return
        words_in_root_line = root_line.split('،')
        root = words_in_root_line[0].strip()
        second_word = words_in_root_line[1].strip() if len(words_in_root_line) > 1 else ''

        word_before_text = self.extract_word_before_colon(section)
        word_before_text = word_before_text if word_before_text else ''

        # تجاهل إذا كانت الكلمة تبدأ بـ "("
        if word_before_text.startswith('('):
            return

        comparison_result = ''
        word_to_compare = second_word if second_word else root
        if word_before_text:
            comparison_result = self.compare_words(word_to_compare, word_before_text)
            comparison_result = self.map_comparison_result(comparison_result)
            # كتابة فقط إذا كان هناك اختلاف في التشكيل
            if comparison_result == '[اختلاف تشكيل]':
                output_file.write(f"{word_to_compare} = {word_before_text} {comparison_result}\n")

    def read_file_content(self, input_file_path):
        """Reads the content of the input file."""
        try:
            with open(input_file_path, encoding="utf8") as file:
                return file.read()
        except FileNotFoundError:
            print(f"لم يتم العثور على الملف: {input_file_path}")
            return None

    def process_file(self, input_file_path, output_file):
        """Processes the entire file and writes the mismatches to the output file."""
        content = self.read_file_content(input_file_path)
        if content is None:
            return
        sections = content.split("تاريخ آخر تحديث")
        for section in sections:
            self.process_section(section, output_file)

def main():
    processor = TextProcessor()
    input_file_path = "جذاذة.txt"
    output_file_path = "مطابق الفرع بالمدخل.txt"

    intro_sentence = "-------------------------مطابقة الفرع بالمدخل--------------------------\n\n"

    try:
        with open(output_file_path, "w", encoding="utf8") as output_file:
            output_file.write(intro_sentence)  # كتابة الجملة الافتتاحية
            processor.process_file(input_file_path, output_file)  # معالجة الملف
        print(f"تمت معالجة الملف بنجاح. النتائج محفوظة في '{output_file_path}'.")
    except IOError as e:
        print(f"حدث خطأ أثناء الكتابة إلى الملف: {e}")

if __name__ == "__main__":
    main()
