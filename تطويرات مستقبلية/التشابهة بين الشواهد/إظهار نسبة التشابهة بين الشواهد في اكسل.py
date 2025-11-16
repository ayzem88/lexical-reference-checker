import pandas as pd
from fuzzywuzzy import fuzz

# قراءة الملف
file_path = "الشواهد.xlsx"
df = pd.read_excel(file_path, header=None)

# استخدام العمود A (العمود 0) كعمود للجمل
sentences_column = 0

# التأكد من وجود عمود C وإن لم يكن موجودًا، نضيفه
if len(df.columns) < 3:
    df[2] = ''  # إضافة عمود C للملاحظات
else:
    df[2] = df[2].astype(str)  # تأكد من أن العمود C هو نوع بيانات string

# إجراء المقارنة الضبابية
for i in range(len(df)):
    similar_sentences = []
    for j in range(len(df)):
        if i != j:
            similarity = fuzz.ratio(df[sentences_column][i], df[sentences_column][j])
            if similarity >= 80:
                similar_sentences.append(similarity)
    
    if similar_sentences:
        average_similarity = sum(similar_sentences) / len(similar_sentences)
        df.at[i, 2] = f'متوسط التشابه: {average_similarity:.2f}%, عدد التشابهات: {len(similar_sentences)}'

# حفظ النتائج في ملف جديد
output_path = "معالجة الشواهد.xlsx"
df.to_excel(output_path, index=False, header=False)
