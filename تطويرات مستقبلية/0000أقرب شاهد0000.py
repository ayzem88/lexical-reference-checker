import re
import openpyxl
from fuzzywuzzy import fuzz

class TextExtractor:
    def __init__(self, txt_file_path):
        self.txt_file_path = txt_file_path
        self.start_pattern = re.compile(r'ن?\d{1,4}هـ/\d{1,4}م.*|ن?\d{1,4}ق\.هـ/\d{1,4}م.*')
        self.end_pattern = re.compile(r'.*\(ت، \d{2,4}هـ\)|^.*،\ ط\d{1,9}،|^.*تحقيق|مراجعة|تقديم|ترجمة|تح|حواشيه|نشرها|نشره|رواية|ديوان|شعر:.*')
        self.exclude_patterns = [r'^".*"$', r'^قَالَ يَ.*', r'^قَالَ يُ.*', r'^قَالَتْ تَ.*', r'^قَالَتْ تُ.*']
    def extract_text(self):
        with open(self.txt_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        records = content.split("تاريخ آخر تحديث")
        results = []
        for record in records:
            start = self.start_pattern.search(record)
            if start:
                end = self.end_pattern.search(record, start.end())
                if end:
                    text = record[start.end():end.start()].split('\n')
                    text = text[:-2]
                    filtered_text = [line for line in text if not any(re.match(ep, line) for ep in self.exclude_patterns)]
                    filtered_text = [line for line in filtered_text if not self.start_pattern.match(line)]
                    if ''.join(filtered_text).strip():
                        results.append('\n'.join(filtered_text))
        with open('مراجعة الشواهد.txt', 'w', encoding='utf-8') as result_file:
            for result in results:
                result_file.write(result + '\n\n')
class TextComparator:
    def __init__(self, txt_file_path, xlsx_file_path, output_file_path):
        self.txt_file_path = txt_file_path
        self.xlsx_file_path = xlsx_file_path
        self.output_file_path = output_file_path
    def compare_texts(self):
        with open(self.txt_file_path, 'r', encoding='utf-8') as file:
            txt_lines = file.readlines()
        workbook = openpyxl.load_workbook(self.xlsx_file_path)
        sheet = workbook.active
        xlsx_lines = [row[0] for row in sheet.iter_rows(min_row=1, max_col=1, values_only=True) if row[0]]
        with open(self.output_file_path, 'w', encoding='utf-8') as output_file:
            for txt_line in txt_lines:
                found_match = False
                for xlsx_line in xlsx_lines:
                    similarity = fuzz.ratio(txt_line.strip(), xlsx_line.strip())
                    if similarity >= 80:
                        output_file.write(f"{txt_line.strip()} - {xlsx_line} = [نسبة التطابق هي {similarity}%]\n\n")
                        found_match = True
                        break
                if not found_match:
                    continue
                    #output_file.write(f"{txt_line.strip()} = [لا يوجد تطابق]\n")
extractor = TextExtractor('جذاذة.txt')
extractor.extract_text()
comparator = TextComparator('مراجعة الشواهد.txt', 'الشواهد.xlsx', 'مقارنة الشواهد.txt')
#comparator.write_header("مراجعة المؤلّف.txt", "-------------------------مراجعة المؤلّف--------------------------\n\n")
comparator.compare_texts()
