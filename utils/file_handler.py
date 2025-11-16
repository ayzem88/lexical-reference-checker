"""
معالجة الملفات وقراءتها
"""
from pathlib import Path


class FileHandler:
    """معالجة قراءة وكتابة الملفات"""
    
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
    
    def read_text_file(self, file_path):
        """قراءة ملف نصي بعدة ترميزات"""
        encodings = ['utf-8', 'windows-1256', 'utf-16', 'cp1256']
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            return None, "الملف غير موجود"
        
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc, errors='ignore') as f:
                    return f.read(), None
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        return None, "فشل قراءة الملف"
    
    def save_results(self, content, filename="النتائج.txt"):
        """حفظ النتائج في ملف"""
        output_path = self.output_dir / filename
        self.output_dir.mkdir(exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, str(output_path)
        except Exception as e:
            return False, str(e)
    
    def find_jadha_file(self):
        """البحث عن ملف جذاذة.txt"""
        possible_locations = [
            self.data_dir / "جذاذة.txt",
            self.base_dir / "جذاذة.txt",
        ]
        
        for location in possible_locations:
            if location.exists():
                return location
        
        return None

