import re

class TextExtractor:
    def __init__(self, txt_file_path):
        self.txt_file_path = txt_file_path
        self.start_pattern = re.compile(r'ن?\d{1,4}هـ/\d{1,4}م.*|ن?\d{1,4}ق\.هـ/\d{1,4}م.*')
        self.end_pattern = re.compile(r'.*\(ت، \d{2,4}هـ\)|^.*،\ ط\d{1,9}،|^.*تحقيق|مراجعة|تقديم|ترجمة|تح|حواشيه|نشرها|نشره|رواية|ديوان|شعر:.*')
        self.exclude_patterns = [r'^".*"$', r'^قَالَ يَ.*', r'^قَالَ يُ.*', r'^قَالَتْ تَ.*', r'^قَالَتْ تُ.*', r'^قَالُوا يَ*', r'^قَالَتْ عَ.*', r'^قَالَ عَ.*', r'^كَتَبَ إِلَى.*']
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

# استخدام الكلاس
extractor = TextExtractor('جذاذة.txt')
extractor.extract_text()
