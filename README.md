# المراجع المعجميّ / Lexical Reference Checker

<div dir="rtl">

## نظرة عامة

نظام مراجعة آلي متقدم للنصوص العربية المعجمية باستخدام واجهة رسومية PyQt6. يساعد الباحثين واللغويين في مراجعة النصوص المعجمية واكتشاف الأخطاء المختلفة.

## المميزات

- ✅ واجهة رسومية سهلة الاستخدام
- ✅ 41 سكريبت متخصص لفحص أنواع مختلفة من الأخطاء
- ✅ عرض النص الأصلي والنتائج جنباً إلى جنب
- ✅ تصدير النتائج إلى ملف نصي
- ✅ مراجعة عامة لجميع السكريبتات دفعة واحدة
- ✅ فحوصات شاملة للإملاء والنحو والصيغ النحوية

## التثبيت

### المتطلبات

- Python 3.8 أو أحدث
- PyQt6

### خطوات التثبيت

1. استنسخ المستودع:
```bash
git clone https://github.com/ayzem88/lexical-reference-checker.git
cd lexical-reference-checker
```

2. قم بتثبيت المكتبات المطلوبة:
```bash
pip install -r requirements.txt
```

أو مباشرة:
```bash
pip install PyQt6
```

## الاستخدام

### تشغيل التطبيق

```bash
python run.py
```

### استخدام الواجهة

1. **فتح الملف**: اضغط على زر "فتح ملف جذاذة.txt" لفتح ملف النص المراد مراجعته
   - أو ضع ملف `جذاذة.txt` في مجلد `data/` وسيتم تحميله تلقائياً

2. **تشغيل سكريبت واحد**: اضغط على أي زر من القائمة اليمنى لتشغيل السكريبت المقابل

3. **مراجعة عامة**: اضغط على زر "مراجعة عامة" في الأعلى لتشغيل جميع السكريبتات

4. **تصدير النتائج**: اضغط على زر "تصدير النتائج" لحفظ النتائج في ملف

## هيكل المشروع

```
المراجع المعجميّ/
├── run.py                       # الملف الرئيسي
├── gui/                         # الواجهة الرسومية
│   └── main_window.py          # النافذة الرئيسية
├── scripts/                     # السكريبتات (41 سكريبت)
│   ├── أخطاء إملائية.py
│   ├── وسم اسم الفاعل.py
│   └── [سكريبتات أخرى]
├── utils/                       # الأدوات المساعدة
│   ├── script_runner.py        # تشغيل السكريبتات
│   └── file_handler.py         # معالجة الملفات
├── data/                        # ملفات الإدخال
│   └── جذاذة.txt
├── output/                      # ملفات المخرجات
├── img-01.png                   # صورة توضيحية 1
├── img-02.png                   # صورة توضيحية 2
└── img-03.png                   # صورة توضيحية 3
```

## أنواع الفحوصات

### فحوصات إملائية ونحوية
- أخطاء إملائية
- حذف حركات السجع
- تكرر الكلمات المتجاورات

### فحوصات الإحالة والمراجع
- الإحالة
- إحالة خاطئة
- أرقام الصفحات

### فحوصات التوثيق والتاريخ
- تاريخ استعمال بعد 1880
- تاريخ استعمال دون ملاحظة نشر
- توثيق الآية الداخلي

### فحوصات الصيغ النحوية
- وسم اسم الفاعل
- وسم اسم المفعول
- وسم اسم التفضيل
- وسم اسم الزمان
- وسم اسم المكان
- وسم اسم المرة
- وسم اسم الهيئة
- وسم الاسم المصغر
- وسم الاسم المنسوب
- وسم الصفة
- وسم الصفة المشبهة
- وسم صيغة المبالغة
- وسم المصدر
- وسم المصدر الميمي
- وسم المصدر الصناعي
- وسم بالفعل اللازم

### فحوصات أخرى
- إضافة الفاعل للفعل اللازم
- الاسم المفعول-الأفعال المتعدية
- المتعدي بالحرف مع المتعدي
- الممنوع من الصرف
- مطابقة الفرع بالمدخل
- دخول الألف واللام على الفرع
- تقدمة للمباني
- قال ليس بعدها فعل مضارع
- ملاحظات النشر
- تعريف اسم التفضيل

## ملاحظات مهمة

- تأكد من وجود ملف `جذاذة.txt` قبل تشغيل السكريبتات
- النتائج تظهر في مربع النتائج بعد انتهاء التشغيل
- يمكن تصدير النتائج في أي وقت
- الخط المستخدم: Sajjala Majala

## التطوير المستقبلي

- [ ] إضافة المزيد من السكريبتات
- [ ] تحسين دقة الفحوصات
- [ ] دعم المزيد من صيغ النصوص
- [ ] واجهة مستخدم محسنة

## المساهمة

نرحب بمساهماتكم! يرجى قراءة [CONTRIBUTING.md](CONTRIBUTING.md) للمزيد من التفاصيل.

## الترخيص

هذا المشروع مخصص للاستخدام الأكاديمي والبحثي.

## المطور

تم تطوير هذا المشروع بواسطة **أيمن الطيّب بن نجي** ([ayzem88](https://github.com/ayzem88))

---

# [English]

<div dir="ltr">

## Overview

An advanced automated review system for Arabic lexical texts using a PyQt6 graphical interface. Helps researchers and linguists review lexical texts and discover various errors.

## Features

- ✅ Easy-to-use graphical interface
- ✅ 41 specialized scripts for checking different types of errors
- ✅ Display original text and results side by side
- ✅ Export results to text file
- ✅ General review of all scripts at once
- ✅ Comprehensive checks for spelling, grammar, and grammatical forms

## Installation

### Requirements

- Python 3.8 or later
- PyQt6

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/ayzem88/lexical-reference-checker.git
cd lexical-reference-checker
```

2. Install required libraries:
```bash
pip install -r requirements.txt
```

Or directly:
```bash
pip install PyQt6
```

## Usage

### Running the Application

```bash
python run.py
```

### Using the Interface

1. **Open File**: Click the "Open جذاذة.txt file" button to open the text file to be reviewed
   - Or place the `جذاذة.txt` file in the `data/` folder and it will be loaded automatically

2. **Run Single Script**: Click any button from the right menu to run the corresponding script

3. **General Review**: Click the "General Review" button at the top to run all scripts

4. **Export Results**: Click the "Export Results" button to save results to a file

## Project Structure

```
lexical-reference-checker/
├── run.py                       # Main file
├── gui/                         # Graphical interface
│   └── main_window.py          # Main window
├── scripts/                     # Scripts (41 scripts)
│   ├── أخطاء إملائية.py
│   ├── وسم اسم الفاعل.py
│   └── [Other scripts]
├── utils/                       # Helper utilities
│   ├── script_runner.py        # Script runner
│   └── file_handler.py         # File handler
├── data/                        # Input files
│   └── جذاذة.txt
├── output/                      # Output files
├── img-01.png                   # Screenshot 1
├── img-02.png                   # Screenshot 2
└── img-03.png                   # Screenshot 3
```

## Types of Checks

### Spelling and Grammar Checks
- Spelling errors
- Missing diacritical marks
- Adjacent word repetition

### Reference and Citation Checks
- Citations
- Incorrect citations
- Page numbers

### Documentation and Date Checks
- Usage date after 1880
- Usage date without publication note
- Internal verse documentation

### Grammatical Form Checks
- Tagging active participle
- Tagging passive participle
- Tagging comparative
- Tagging time noun
- Tagging place noun
- Tagging instance noun
- Tagging state noun
- Tagging diminutive
- Tagging relative adjective
- Tagging adjective
- Tagging similar adjective
- Tagging intensive form
- Tagging verbal noun
- Tagging mimic verbal noun
- Tagging artificial verbal noun
- Tagging with intransitive verb

### Other Checks
- Adding subject to intransitive verb
- Passive participle - transitive verbs
- Transitive with preposition vs transitive
- Non-declinable
- Matching branch with entry
- Definite article on branch
- Introduction to patterns
- "قال" without following present verb
- Publication notes
- Defining comparative

## Important Notes

- Make sure the `جذاذة.txt` file exists before running scripts
- Results appear in the results box after completion
- Results can be exported at any time
- Font used: Sajjala Majala

## Future Development

- [ ] Add more scripts
- [ ] Improve check accuracy
- [ ] Support more text formats
- [ ] Enhanced user interface

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is intended for academic and research use.

## Development Approach

I adopt the Vibe Coding paradigm in my software projects: rather than writing every line manually, I direct AI models with clear natural-language descriptions of the desired functionality, then evaluate and refine the generated code.

This approach accelerates prototype and module creation, allowing me to focus more on concept and design than on low-level implementation details.

In this repository you'll find tools and projects developed with this mindset — feel free to explore and contribute.

## Developer

Developed by **Ayman Atieb ben NJi** ([ayzem88](https://github.com/ayzem88))

</div>

