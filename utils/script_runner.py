"""
نظام تشغيل السكريبتات وقراءة النتائج
"""
import subprocess
import os
import sys
from pathlib import Path


class ScriptRunner:
    """تشغيل السكريبتات وقراءة النتائج"""
    
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        self.base_dir = Path(base_dir)
        self.scripts_dir = self.base_dir / "scripts"
        self.output_dir = self.base_dir / "output"
        self.data_dir = self.base_dir / "data"
        
        # إنشاء المجلدات إذا لم تكن موجودة
        self.output_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
    
    def get_script_path(self, script_name):
        """الحصول على مسار السكريبت"""
        # البحث في مجلد scripts أولاً
        script_path = self.scripts_dir / script_name
        if script_path.exists():
            return script_path
        
        # البحث في المجلد الرئيسي
        script_path = self.base_dir / script_name
        if script_path.exists():
            return script_path
        
        return None
    
    def run_script(self, script_name):
        """
        تشغيل سكريبت معين وإرجاع النتائج
        
        Args:
            script_name: اسم السكريبت
            
        Returns:
            tuple: (success: bool, output: str, error: str)
        """
        script_path = self.get_script_path(script_name)
        
        if not script_path:
            return False, "", f"السكريبت '{script_name}' غير موجود"
        
        try:
            # تغيير المجلد الحالي إلى المجلد الرئيسي
            original_dir = os.getcwd()
            os.chdir(self.base_dir)
            
            # تشغيل السكريبت
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            # العودة للمجلد الأصلي
            os.chdir(original_dir)
            
            if result.returncode == 0:
                # البحث عن ملف النتائج
                output_file = self.find_output_file(script_name)
                if output_file:
                    output_content = self.read_output_file(output_file)
                    return True, output_content, ""
                else:
                    return True, "", "تم التشغيل بنجاح لكن لم يتم العثور على ملف النتائج"
            else:
                return False, "", result.stderr or "حدث خطأ أثناء التشغيل"
                
        except Exception as e:
            return False, "", str(e)
    
    def find_output_file(self, script_name):
        """البحث عن ملف النتائج للسكريبت"""
        script_base = script_name.replace('.py', '')
        
        # قائمة بأسماء ملفات النتائج المحتملة بناءً على اسم السكريبت
        possible_names = []
        
        # الأسماء الشائعة بناءً على نوع السكريبت
        if script_base.startswith('وسم '):
            possible_names.extend([
                f"خطأ في {script_base}.txt",
                f"خطأ في وسم {script_base.replace('وسم ', '')}.txt",
                f"{script_base}.txt",
            ])
        elif 'خطأ' in script_base or 'ملاحظات' in script_base:
            possible_names.append(f"{script_base}.txt")
        else:
            # أسماء عامة
            possible_names.extend([
                f"{script_base}.txt",
                f"خطأ في {script_base}.txt",
                f"ملاحظات على {script_base}.txt",
            ])
        
        # إضافة أسماء خاصة لبعض السكريبتات
        special_names = {
            'أخطاء إملائية': ['الأخطاء الإملائية.txt'],
            'أرقام الصفحات': ['مصادر دون أرقام صفحات.txt'],
            'إحالة خاطئة': ['إحالات خاطئة.txt'],
            'إضافة الفاعل للفعل اللازم': ['إضافة الفاعل للفعل اللازم.txt'],
            'الإحالة': ['جذاذات دون إحالة.txt'],
            'الاسم المفعول-الأفعال المتعدية': ['ملاحظات على الاسم المفعول.txt'],
            'المتعدي بالحرف مع المتعدي': ['المتعدي بالحرف مع المتعدي.txt'],
            'الممنوع من الصرف': ['الممنوع من الصرف.txt'],
            'تاريخ استعمال بعد 1880': ['تاريخ استعمال بعد 1880.txt'],
            'تاريخ استعمال دون ملاحظة نشر': ['تاريخ استعمال.txt'],
            'تعريف اسم التفضيل': ['خطأ في تعريف اسم التفضيل.txt'],
            'تقدمة للمباني': ['تقدمة للمباني.txt'],
            'تكرر الكلمات المتجاورات': ['تكرار الكلمة.txt'],
            'توثيق الآية الداخلي': ['توثيق الآية الداخلي.txt'],
            'حذف حركات السجع': ['ملاحظات حركات السجع.txt'],
            'دخول الألف واللام على الفرع': ['دخول الألف واللام على الفرع.txt'],
            'قال ليس بعدها فعل مضارع': ['قال ليس بعدها فعل مضارع.txt'],
            'مطابقة الفرع بالمدخل': ['مطابق الفرع بالمدخل.txt'],
            'ملاحظات النشر': ['ملاحظات النشر غير المنمطة.txt'],
        }
        
        if script_base in special_names:
            possible_names = special_names[script_base] + possible_names
        
        # البحث في المجلد الرئيسي أولاً
        for name in possible_names:
            file_path = self.base_dir / name
            if file_path.exists():
                return file_path
        
        # البحث في مجلد output
        for name in possible_names:
            file_path = self.output_dir / name
            if file_path.exists():
                return file_path
        
        # البحث عن أي ملف txt جديد (عدا جذاذة.txt)
        txt_files = list(self.base_dir.glob('*.txt'))
        txt_files = [f for f in txt_files if 'جذاذة' not in f.name and 'الملاحظات' not in f.name]
        
        if txt_files:
            # إرجاع أحدث ملف
            return max(txt_files, key=lambda p: p.stat().st_mtime)
        
        return None
    
    def read_output_file(self, file_path):
        """قراءة ملف النتائج بعدة ترميزات"""
        encodings = ['utf-8', 'windows-1256', 'utf-16', 'cp1256']
        
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc, errors='ignore') as f:
                    return f.read()
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        return "⚠️ لم أتمكن من قراءة الملف"
    
    def run_all_scripts(self):
        """تشغيل جميع السكريبتات"""
        scripts = [
            "أخطاء إملائية.py",
            "أرقام الصفحات.py",
            "إحالة خاطئة.py",
            "إضافة الفاعل للفعل اللازم.py",
            "الإحالة.py",
            "الاسم المفعول-الأفعال المتعدية.py",
            "المتعدي بالحرف مع المتعدي.py",
            "الممنوع من الصرف.py",
            "تاريخ استعمال بعد 1880.py",
            "تاريخ استعمال دون ملاحظة نشر.py",
            "تعريف اسم التفضيل.py",
            "تقدمة للمباني.py",
            "تكرر الكلمات المتجاورات.py",
            "توثيق الآية الداخلي.py",
            "حذف حركات السجع.py",
            "دخول الألف واللام على الفرع.py",
            "قال ليس بعدها فعل مضارع.py",
            "مطابقة الفرع بالمدخل.py",
            "ملاحظات النشر.py",
            "وسم اسم التفضيل.py",
            "وسم اسم الزمان.py",
            "وسم اسم الفاعل.py",
            "وسم اسم المرة.py",
            "وسم اسم المفعول.py",
            "وسم اسم المكان.py",
            "وسم اسم الهيئة.py",
            "وسم الاسم المصغر.py",
            "وسم الاسم المنسوب.py",
            "وسم الصفة المشبهة.py",
            "وسم الصفة.py",
            "وسم المصدر الصناعي.py",
            "وسم المصدر الميمي.py",
            "وسم المصدر.py",
            "وسم بالفعل اللازم.py",
            "وسم صيغة المبالغة.py"
        ]
        
        all_results = []
        
        for script in scripts:
            success, output, error = self.run_script(script)
            if success and output:
                all_results.append(f"\n{'='*80}\n")
                all_results.append(f"# {script}\n")
                all_results.append(f"{'='*80}\n\n")
                all_results.append(output)
                all_results.append("\n\n")
        
        return "\n".join(all_results)

