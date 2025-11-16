import subprocess
import glob2
import os

# ========== تشغيل السكريبتات ==========
scripts = [
    r"أخطاء إملائية.py",
    r"أرقام الصفحات.py",
    r"إحالة خاطئة.py",
    r"إضافة الفاعل للفعل اللازم.py",
    r"الإحالة.py",
    r"الاسم المفعول-الأفعال المتعدية.py",
    r"المتعدي بالحرف مع المتعدي.py",
    r"الممنوع من الصرف.py",
    r"تاريخ استعمال بعد 1880.py",
    r"تاريخ استعمال دون ملاحظة نشر.py",
    r"تعريف اسم التفضيل.py",
    r"تقدمة للمباني.py",
    r"تكرر الكلمات المتجاورات.py",
    r"توثيق الآية الداخلي.py",
    r"حذف حركات السجع.py",
    r"دخول الألف واللام على الفرع.py",
    r"قال ليس بعدها فعل مضارع.py",
    r"مطابقة الفرع بالمدخل.py",
    r"ملاحظات النشر.py",
    r"وسم اسم التفضيل.py",
    r"وسم اسم الزمان.py",
    r"وسم اسم الفاعل.py",
    r"وسم اسم المرة.py",
    r"وسم اسم المفعول.py",
    r"وسم اسم المكان.py",
    r"وسم اسم الهيئة.py",
    r"وسم الاسم المصغر.py",
    r"وسم الاسم المنسوب.py",
    r"وسم الصفة المشبهة.py",
    r"وسم الصفة.py",
    r"وسم المصدر الصناعي.py",
    r"وسم المصدر الميمي.py",
    r"وسم المصدر.py",
    r"وسم بالفعل اللازم.py",
    r"وسم صيغة المبالغة.py"
]

for script in scripts:
    print(f"▶️ جاري تشغيل: {script}")
    subprocess.run(["python3", script])

# ========== جمع النتائج ==========
filenames = glob2.glob('*.txt')
filtered_filenames = [file for file in filenames if "جذاذة" not in file]

# دالة لفتح الملف بعدة ترميزات
def read_file_with_multiple_encodings(filename):
    encodings = ['utf-8', 'windows-1256', 'utf-16']
    for enc in encodings:
        try:
            with open(filename, encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    print(f"⚠️ لم أتمكن من قراءة الملف: {filename}")
    return ""

with open('الملاحظات.txt', 'w', encoding='utf-8') as f:
    for file in filtered_filenames:
        content = read_file_with_multiple_encodings(file)
        if content:
            f.write(content + '\n')

# ========== حذف الملفات المؤقتة ==========
for file in filtered_filenames:
    if file not in ["جذاذة.txt", "الملاحظات.txt"]:
        os.remove(file)
