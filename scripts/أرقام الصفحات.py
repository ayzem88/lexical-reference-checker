import re

def extract_new_case_lines(record):
    new_pattern = r'.*\(\d+[هـمه].*\d+\.'  # النمط الأساسي للبحث
    alternative_pattern = r'.*\(\d+[هـمه].*\..*'  # النمط البديل للطباعة إذا لم يتم العثور على النمط الأساسي
    header_pattern = r'^\w{3,4}\،\ .*\،\ .*$'  # النمط لرأس السجل

    if not re.search(new_pattern, record, re.M):
        alternative_matches = re.findall(alternative_pattern, record, re.M)
        if alternative_matches:
            header_match = re.search(header_pattern, record, re.M)
            header_line = header_match.group(0) if header_match else "No Header Found"
            return alternative_matches + [header_line]
    return []

def save_results_to_file(filename, new_case_lines):
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write("-------------------------مصادر دون أرقام صفحات-------------------------\n\n")
        for line in new_case_lines:
            output_file.write(line + "\n\n")

if __name__ == "__main__":
    with open("جذاذة.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    records = content.split("تاريخ آخر تحديث")

    lines_new_case = []

    for record in records:
        result = extract_new_case_lines(record)
        if result:
            lines_new_case.extend(result)

    save_results_to_file("مصادر دون أرقام صفحات.txt", lines_new_case)

