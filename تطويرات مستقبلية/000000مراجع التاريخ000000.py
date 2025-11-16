import re
import os
import pandas as pd
from fuzzywuzzy import fuzz
import openpyxl


class TextProcessor:
    def __init__(self):
        self.preceding_pattern = r'.*\(ت، \d{2,4}هـ\)|^.*،\ ط\d{1,9}،|^.*تحقيق|مراجعة|تقديم|ترجمة|تح|حواشيه|نشرها|نشره|رواية|ديوان|شعر:.*'
        self.date_pattern = r'ن?\d{1,4}هـ/\d{1,4}م|ن?\d{1,4}ق\.هـ/\d{1,4}م'      
        self.pattern_to_print = r'^\w{3,4}\،\ .*\،\ .*$'

    def extract_authors(self, file_path):
        authors = {}
        record_header = ""
        with open(file_path, 'r', encoding='utf-8') as file:
            record = []
            for line in file:
                if re.match(self.pattern_to_print, line):
                    record_header = line.strip()
                record.append(line.strip())
                if 'تاريخ آخر تحديث' in line:
                    author, date = None, None
                    for i, line in enumerate(record):
                        if re.match(self.preceding_pattern, line):
                            author = record[i - 1].strip()
                        elif re.match(self.date_pattern, line):
                            date = re.search(self.date_pattern, line).group()
                    if author and date:
                        authors[author] = (date, record_header)
                    record = []
        return authors

class ExcelProcessor:
   
    @staticmethod
    def read_excel_file(file_path):
        authors = {}
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] is not None and row[1] is not None:
                authors[row[0].strip()] = row[1].strip()
        return authors

class AuthorComparer:
    @staticmethod
    def calculate_year_difference(date1, date2):
        year1 = int(date1.split('/')[1].strip('م')) if '/' in date1 and 'م' in date1 else None
        year2 = int(date2.split('/')[1].strip('م')) if '/' in date2 and 'م' in date2 else None
        return abs(year1 - year2) if year1 and year2 else None
    
    @staticmethod
    def is_date_after_death(date1, date2):
        year1 = int(date1.split('/')[1].strip('م')) if '/' in date1 and 'م' in date1 else None
        year2 = int(date2.split('/')[1].strip('م')) if '/' in date2 and 'م' in date2 else None
        return year1 > year2 if year1 and year2 else False

    @staticmethod
    def both_dates_start_with_n(date1, date2):
        return date1.startswith('ن') and date2.startswith('ن')
    
    @staticmethod
    def compare_authors(txt_authors, excel_authors):
        results_not_found = []
        results_other = []
        for author, (date, header) in txt_authors.items():
            result_line = header + "\n"
            if author in excel_authors:
                if date == excel_authors[author]:
                    # كما في السابق
                    continue
                else:
                    year_difference = AuthorComparer.calculate_year_difference(date, excel_authors[author])
                    extra_note = " (!أكثر من 85 سنة)" if year_difference and year_difference > 85 else ""
                    if AuthorComparer.is_date_after_death(date, excel_authors[author]):
                        extra_note += " (تاريخ بعد الوفاة !)"
                    if AuthorComparer.both_dates_start_with_n(date, excel_authors[author]):
                        extra_note += " (تاريخا وفاة!)"
                    result_line += f"{author} {date} |x| {author} {excel_authors[author]} = [الاسم موجود] = [التاريخ غير مطابق]{extra_note}\n"
                    results_other.append(result_line)
            else:
                # استخدام fuzzy matching للعثور على تطابقات نسبية
                highest_match = 0
                matched_author = None
                for excel_author in excel_authors.keys():
                    match_score = fuzz.ratio(author, excel_author)
                    if match_score > highest_match:
                        highest_match = match_score
                        matched_author = excel_author
                if highest_match > 90:  # اختر عتبة مناسبة للتطابق
                    # تطابق نسبي
                    # عقد مقارنة التواريخ للأسماء المتطابقة نسبيا
                    year_difference = AuthorComparer.calculate_year_difference(date, excel_authors[matched_author])
                    extra_note = " (أكثر من 85 سنة)" if year_difference and year_difference > 85 else ""
                    if AuthorComparer.is_date_after_death(date, excel_authors[matched_author]):
                        extra_note += " (تاريخ بعد الوفاة !)"
                    if AuthorComparer.both_dates_start_with_n(date, excel_authors[matched_author]):
                        extra_note += " (تاريخا وفاة!!)"
                    result_line += f"{author} {date} |=| {matched_author} {excel_authors[matched_author]} = [الاسم موجود بتطابق نسبي] = [التاريخ غير مطابق]{extra_note}\n"
                    results_other.append(result_line)
                else:
                    # لا يوجد تطابق
                    result_line += f"{author} {date} = [الاسم غير موجود]\n"
                results_not_found.append(result_line)
        return results_not_found + results_other

class FileWriter:
    @staticmethod
    def write_header(file_path, header_line):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(header_line)

    @staticmethod
    def write_results(file_path, results):
        with open(file_path, 'a', encoding='utf-8') as file:
            for result in results:
                file.write(result + '\n')
txt_processor = TextProcessor()
excel_processor = ExcelProcessor()
author_comparer = AuthorComparer()
file_writer = FileWriter()
txt_authors = txt_processor.extract_authors("جذاذة.txt")
excel_authors = excel_processor.read_excel_file("المؤلفون.xlsx")
comparison_results = author_comparer.compare_authors(txt_authors, excel_authors)
file_writer.write_header("مراجع التاريخ.txt", "-------------------------مراجع التاريخ--------------------------\n\n")
file_writer.write_results("مراجع التاريخ.txt", comparison_results)
