import re
import openpyxl
from fuzzywuzzy import fuzz

class TextExtractor:
    def __init__(self, txt_file_path, xlsx_file_path):
        self.txt_file_path = txt_file_path
        self.xlsx_file_path = xlsx_file_path
        self.start_pattern = re.compile(r'ن?\d{1,4}هـ/\d{1,4}م|ن?\d{1,4}ق\.هـ/\d{1,4}م')
        self.end_pattern = re.compile(r'.*\(ت، \d{2,4}هـ\)|^.*،\ ط\d{1,9}،|^.*تحقيق|مراجعة|تقديم|ترجمة|تح|حواشيه|نشرها|نشره|رواية|ديوان|شعر:.*')
        self.exclude_patterns = [re.compile(r'^".*"$'), re.compile(r'^قَالَ يَ.*'), re.compile(r'^قَالَ يُ.*'), re.compile(r'^قَالَتْ تَ.*'),
                                 re.compile(r'^قَالَتْ عَ.*'), re.compile(r'^قَالَ عَ.*'), re.compile(r'^قَالُوا يَ.*'), re.compile(r'^كَتَبَ إِلَى.*')]

    def extract_text(self):
        with open(self.txt_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        records = content.split("تاريخ آخر تحديث")
        results = []
        for record in records:
            date_match = self.start_pattern.search(record)
            if date_match:
                end = self.end_pattern.search(record, date_match.end())
                date = date_match.group()
                text = record[date_match.end():end.start()] if end else record[date_match.end():]
                text_lines = text.split('\n')[1:-2]
                include_line = True
                filtered_text = []
                for line in text_lines:
                    if any(pattern.match(line) for pattern in self.exclude_patterns):
                        include_line = False
                    if include_line:
                        filtered_text.append(line)

                for line in filtered_text:
                    results.append((line, date))
        return results 
    def compare_texts(self, text_date_pairs):
        workbook = openpyxl.load_workbook(self.xlsx_file_path)
        sheet = workbook.active
        xlsx_lines = []
        for row in sheet.iter_rows(min_row=1, values_only=True):
            if row[0] is not None and row[1] is not None:
                xlsx_lines.append((row[0].strip(), row[1].strip()))
        results = []
        for text, date in text_date_pairs:
            found_match = False
            for xlsx_line, xlsx_date in xlsx_lines:
                if text == xlsx_line:
                    found_match = True
                    date_match = "(تاريخ مطابق)" if date == xlsx_date else "(تاريخ غير مطابق!!)"
                    continue
                    #results.append(f"{text} = {date} - {xlsx_line} = {xlsx_date} (مطابقة الشاهد) {date_match}")
                    break
            if not found_match:
                best_match = None
                highest_ratio = 0
                for xlsx_line, xlsx_date in xlsx_lines:
                    ratio = fuzz.ratio(text, xlsx_line)
                    if ratio > highest_ratio:
                        highest_ratio = ratio
                        best_match = (xlsx_line, xlsx_date)
                if highest_ratio >= 90:
                    date_match = "(تاريخ مطابق)" if date == best_match[1] else "(تاريخ غير مطابق!!)"
                    results.append(f"{text} = {date} - {best_match[0]} = {best_match[1]} (مطابقة الشاهد بنسبة {highest_ratio}%) {date_match}")
                else:
                    continue
                   #results.append(f"{text} = {date} (غير مطابق)")
        with open('2مراجعة الشاهد.txt', 'w', encoding='utf-8') as result_file:
            for result in results:
                result_file.write(result + "\n\n")

extractor = TextExtractor('جذاذة.txt', 'الشواهد.xlsx')
text_date_pairs = extractor.extract_text()
extractor.compare_texts(text_date_pairs)
