import re

def find_specific_pattern(input_file):
    # نمط البحث عن ثلاث كلمات وآخرها "اسْمُ مَفْعُول"
    three_words_pattern = r'^\w{3,4}\،\ .*\،\ اسْمُ مَفْعُول$'
    
    # نمط البحث عن "مُتَعَدٍّ" أو "مُتَعَدٍّ بِالحَرْف"
    search_pattern = r'مُتَعَدٍّ|مُتَعَدٍّ بِالحَرْف'
    
    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read()
        
        matches = re.findall(three_words_pattern, data, re.MULTILINE)
        for match in matches:
            # إذا لم نجد "مُتَعَدٍّ" أو "مُتَعَدٍّ بِالحَرْف" في الملف كله بعد العثور على نمط "اسْمُ مَفْعُول"
            if not re.search(search_pattern, data):
                results.append(match)

    return results

# تنفيذ الوظيفة
specific_results = find_specific_pattern("جذاذة.txt")
intro_sentence = "-------------------------مراجعة اسم المفعول لعدم وجود المتعدي--------------"



# حفظ النتائج في ملف جديد
with open("ملاحظات على الاسم المفعول.txt", 'w', encoding='utf-8') as f:
    f.write(intro_sentence + '\n\n')
    f.write('\n'.join(specific_results))
