"""
الواجهة الرئيسية للتطبيق
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QFileDialog, QMessageBox,
    QScrollArea, QLabel, QProgressBar, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QTextCursor, QPainter

from utils.script_runner import ScriptRunner
from utils.file_handler import FileHandler


class DotsHandle(QWidget):
    """Widget مخصص لرسم 3 نقاط في المنتصف"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(20)
        self.setMaximumWidth(20)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # لون النقاط
        painter.setBrush(QColor("#888888"))
        painter.setPen(Qt.PenStyle.NoPen)
        
        # حساب المواضع (3 نقاط في المنتصف)
        width = self.width()
        height = self.height()
        dot_size = 4
        spacing = 6
        total_height = (dot_size * 3) + (spacing * 2)
        start_y = (height - total_height) / 2
        
        # رسم 3 نقاط
        for i in range(3):
            y = start_y + (i * (dot_size + spacing)) + (dot_size / 2)
            painter.drawEllipse(int(width / 2 - dot_size / 2), int(y - dot_size / 2), dot_size, dot_size)


class ScriptWorker(QThread):
    """عامل لتشغيل السكريبتات في خيط منفصل"""
    finished = pyqtSignal(bool, str, str)  # success, output, error
    
    def __init__(self, script_name, runner):
        super().__init__()
        self.script_name = script_name
        self.runner = runner
    
    def run(self):
        success, output, error = self.runner.run_script(self.script_name)
        self.finished.emit(success, output, error)


class AllScriptsWorker(QThread):
    """عامل لتشغيل جميع السكريبتات"""
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)  # script name
    
    def __init__(self, runner):
        super().__init__()
        self.runner = runner
    
    def run(self):
        result = self.runner.run_all_scripts()
        self.finished.emit(result)


class MainWindow(QMainWindow):
    """النافذة الرئيسية"""
    
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).parent.parent
        self.runner = ScriptRunner(self.base_dir)
        self.file_handler = FileHandler(self.base_dir)
        self.current_file_path = None
        
        self.init_ui()
        self.load_jadha_file()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        self.setWindowTitle("المراجع الآلي - نظام مراجعة النصوص العربية")
        self.setGeometry(100, 100, 1400, 900)
        
        # تعيين الخط الافتراضي - Sajjala Majala
        self.default_font = QFont("Sajjala Majala", 14)
        self.default_font.setBold(False)
        
        # الويدجت المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #f5f5f5;")
        
        # التخطيط الرئيسي (أفقي)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # ========== القسم الأيمن: قائمة الأزرار ==========
        buttons_panel = QWidget()
        buttons_panel.setFixedWidth(280)
        buttons_panel.setStyleSheet("background-color: #e8e8e8;")
        buttons_main_layout = QVBoxLayout(buttons_panel)
        buttons_main_layout.setSpacing(8)
        buttons_main_layout.setContentsMargins(8, 8, 8, 8)
        
        # زر مراجعة عامة (خارج ScrollArea)
        btn_general = QPushButton("مراجعة عامة")
        btn_general.setMinimumHeight(55)
        btn_general.setFont(self.default_font)
        btn_general.setStyleSheet("""
            QPushButton {
                background-color: #d0d0d0;
                color: #000000;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #b0b0b0;
                border-radius: 3px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
            QPushButton:pressed {
                background-color: #b0b0b0;
            }
        """)
        btn_general.clicked.connect(self.run_all_scripts)
        buttons_main_layout.addWidget(btn_general)
        
        # خط فاصل (خارج ScrollArea)
        separator = QLabel("─" * 35)
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        separator.setFont(self.default_font)
        separator.setStyleSheet("color: #888888;")
        buttons_main_layout.addWidget(separator)
        
        # ScrollArea لقائمة الأزرار
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #e8e8e8;
            }
            QScrollBar:vertical {
                background-color: #d0d0d0;
                width: 12px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: #a0a0a0;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #909090;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Widget داخلي للـ ScrollArea يحتوي على الأزرار
        buttons_scroll_widget = QWidget()
        buttons_scroll_widget.setStyleSheet("background-color: #e8e8e8;")
        buttons_layout = QVBoxLayout(buttons_scroll_widget)
        buttons_layout.setSpacing(8)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # قائمة الأزرار
        self.script_buttons = []
        scripts = [
            "أخطاء إملائية",
            "أرقام الصفحات",
            "إحالة خاطئة",
            "إضافة الفاعل للفعل اللازم",
            "الإحالة",
            "الاسم المفعول-الأفعال المتعدية",
            "المتعدي بالحرف مع المتعدي",
            "الممنوع من الصرف",
            "تاريخ استعمال بعد 1880",
            "تاريخ استعمال دون ملاحظة نشر",
            "تعريف اسم التفضيل",
            "تقدمة للمباني",
            "تكرر الكلمات المتجاورات",
            "توثيق الآية الداخلي",
            "حذف حركات السجع",
            "دخول الألف واللام على الفرع",
            "قال ليس بعدها فعل مضارع",
            "مطابقة الفرع بالمدخل",
            "ملاحظات النشر",
            "وسم اسم التفضيل",
            "وسم اسم الزمان",
            "وسم اسم الفاعل",
            "وسم اسم المرة",
            "وسم اسم المفعول",
            "وسم اسم المكان",
            "وسم اسم الهيئة",
            "وسم الاسم المصغر",
            "وسم الاسم المنسوب",
            "وسم الصفة المشبهة",
            "وسم الصفة",
            "وسم المصدر الصناعي",
            "وسم المصدر الميمي",
            "وسم المصدر",
            "وسم بالفعل اللازم",
            "وسم صيغة المبالغة"
        ]
        
        for script_name in scripts:
            btn = QPushButton(script_name)
            btn.setMinimumHeight(40)
            btn.setFont(self.default_font)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    color: #000000;
                    text-align: right;
                    padding: 8px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:pressed {
                    background-color: #c0c0c0;
                }
            """)
            btn.clicked.connect(lambda checked, name=script_name: self.run_script(name))
            buttons_layout.addWidget(btn)
            self.script_buttons.append(btn)
        
        buttons_layout.addStretch()
        
        # تعيين الـ widget للـ ScrollArea
        scroll_area.setWidget(buttons_scroll_widget)
        
        # إضافة ScrollArea إلى التخطيط الرئيسي
        buttons_main_layout.addWidget(scroll_area)
        
        # ========== القسم الأوسط والأيسر: Splitter ==========
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)  # منع إخفاء الأقسام بالكامل
        splitter.setHandleWidth(20)  # عرض أكبر لاستيعاب النقاط
        splitter.setOpaqueResize(True)  # تحديث فوري عند السحب
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #f5f5f5;
                border: none;
            }
            QSplitter::handle:hover {
                background-color: #e8e8e8;
            }
            QSplitter::handle:horizontal {
                width: 20px;
                margin: 0px;
            }
        """)
        
        # مربع النص الأصلي (الوسط)
        original_text_widget = QWidget()
        original_text_widget.setStyleSheet("background-color: #f5f5f5;")
        original_text_layout = QVBoxLayout(original_text_widget)
        original_text_layout.setContentsMargins(8, 8, 8, 8)
        original_text_layout.setSpacing(8)
        
        # زر استيراد الجذاذة وزر المسح - في الأعلى على اليمين
        btn_open_header = QHBoxLayout()
        btn_open_header.addStretch()  # مسافة من اليسار
        
        # زر المسح
        btn_clear = QPushButton("مسح")
        btn_clear.setFont(self.default_font)
        btn_clear.setFixedHeight(35)  # نفس ارتفاع زر التصدير
        btn_clear.setMinimumWidth(100)
        btn_clear.setMaximumWidth(120)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                padding: 8px 15px;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        btn_clear.clicked.connect(self.clear_file)
        btn_open_header.addWidget(btn_clear)
        
        # زر استيراد الجذاذة
        btn_open = QPushButton("استيراد الجذاذة")
        btn_open.setFont(self.default_font)
        btn_open.setFixedHeight(35)  # نفس ارتفاع زر التصدير
        btn_open.setMinimumWidth(160)
        btn_open.setMaximumWidth(180)
        btn_open.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                padding: 8px 15px;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        btn_open.clicked.connect(self.open_file)
        btn_open_header.addWidget(btn_open)
        original_text_layout.addLayout(btn_open_header)
        
        self.original_text = QTextEdit()
        self.original_text.setReadOnly(True)
        self.original_text.setFont(QFont("Sajjala Majala", 14))
        self.original_text.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #c0c0c0;
                color: #000000;
                font-size: 14px;
            }
        """)
        original_text_layout.addWidget(self.original_text)
        
        splitter.addWidget(original_text_widget)
        
        # مربع النتائج (الأيسر)
        results_widget = QWidget()
        results_widget.setStyleSheet("background-color: #f5f5f5;")
        results_layout = QVBoxLayout(results_widget)
        results_layout.setContentsMargins(8, 8, 8, 8)
        results_layout.setSpacing(8)
        
        # زر التصدير - في الأعلى على اليمين
        btn_export_header = QHBoxLayout()
        btn_export_header.addStretch()  # مسافة من اليسار
        btn_export = QPushButton("تصدير النتائج")
        btn_export.setFont(self.default_font)
        btn_export.setFixedHeight(35)  # نفس ارتفاع زر الاستيراد
        btn_export.setMinimumWidth(160)
        btn_export.setMaximumWidth(180)
        btn_export.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                padding: 8px 15px;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        btn_export.clicked.connect(self.export_results)
        btn_export_header.addWidget(btn_export)
        results_layout.addLayout(btn_export_header)
        
        # شريط التقدم
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #e0e0e0;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #b0b0b0;
            }
        """)
        results_layout.addWidget(self.progress_bar)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Sajjala Majala", 14))
        self.results_text.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #c0c0c0;
                color: #000000;
                font-size: 14px;
            }
        """)
        results_layout.addWidget(self.results_text)
        
        splitter.addWidget(results_widget)
        
        # تعيين النسب (50% للنص الأصلي، 50% للنتائج - متساويان)
        splitter.setSizes([500, 500])
        splitter.setStretchFactor(0, 1)  # النص الأصلي
        splitter.setStretchFactor(1, 1)  # النتائج
        
        # استبدال الـ handle بالنقاط المخصصة
        for i in range(splitter.count() - 1):
            handle = splitter.handle(i)
            if handle:
                # إنشاء widget النقاط
                dots_widget = DotsHandle(handle)
                # إضافة widget النقاط إلى الـ handle
                handle_layout = QVBoxLayout(handle)
                handle_layout.setContentsMargins(0, 0, 0, 0)
                handle_layout.addWidget(dots_widget)
        
        # إضافة Splitter قبل الأزرار (الأزرار ستكون على اليمين)
        main_layout.addWidget(splitter, stretch=1)
        
        # إضافة القسم الأيمن (الأزرار) في النهاية
        main_layout.addWidget(buttons_panel)
    
    def load_jadha_file(self):
        """تحميل ملف جذاذة.txt تلقائياً"""
        jadha_path = self.file_handler.find_jadha_file()
        if jadha_path:
            self.load_file(str(jadha_path))
    
    def open_file(self):
        """فتح ملف جذاذة.txt"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "فتح ملف جذاذة.txt",
            str(self.base_dir),
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """تحميل ملف وعرضه"""
        content, error = self.file_handler.read_text_file(file_path)
        
        if error:
            QMessageBox.warning(self, "خطأ", f"فشل قراءة الملف:\n{error}")
            return
        
        self.current_file_path = file_path
        self.original_text.setPlainText(content)
        
        # نسخ الملف إلى المجلد الرئيسي باسم جذاذة.txt
        # (جميع السكريبتات تبحث عن جذاذة.txt)
        target_path = self.base_dir / "جذاذة.txt"
        source_path = Path(file_path)
        
        # نسخ الملف إذا كان مختلفاً عن الهدف
        if source_path != target_path:
            try:
                import shutil
                shutil.copy2(file_path, target_path)
            except Exception as e:
                QMessageBox.warning(self, "تحذير", f"تم تحميل الملف لكن فشل نسخه:\n{str(e)}")
    
    def clear_file(self):
        """مسح الملف المستورد والنتائج"""
        self.original_text.clear()
        self.results_text.clear()
        self.current_file_path = None
        
        # حذف ملف جذاذة.txt من المجلد الرئيسي إذا كان موجوداً
        target_path = self.base_dir / "جذاذة.txt"
        if target_path.exists():
            try:
                target_path.unlink()
            except Exception as e:
                print(f"تحذير: لم يتم حذف الملف: {e}")
    
    def run_script(self, script_name):
        """تشغيل سكريبت معين"""
        if not self.current_file_path:
            QMessageBox.warning(self, "تحذير", "يرجى استيراد ملف النص أولاً")
            return
        
        # إضافة .py إذا لم يكن موجوداً
        script_file = script_name + ".py"
        
        # عرض شريط التقدم
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # indeterminate
        
        # تعطيل الأزرار
        for btn in self.script_buttons:
            btn.setEnabled(False)
        
        # تشغيل السكريبت في خيط منفصل
        self.worker = ScriptWorker(script_file, self.runner)
        self.worker.finished.connect(self.on_script_finished)
        self.worker.start()
    
    def on_script_finished(self, success, output, error):
        """عند انتهاء تشغيل السكريبت"""
        # إخفاء شريط التقدم
        self.progress_bar.setVisible(False)
        
        # تفعيل الأزرار
        for btn in self.script_buttons:
            btn.setEnabled(True)
        
        if success:
            if output:
                self.results_text.setPlainText(output)
                self.format_results(output)
            else:
                self.results_text.setPlainText("تم التشغيل بنجاح لكن لا توجد نتائج")
        else:
            QMessageBox.critical(self, "خطأ", f"فشل تشغيل السكريبت:\n{error}")
            self.results_text.setPlainText(f"خطأ: {error}")
    
    def format_results(self, text):
        """تنسيق النتائج"""
        # يمكن إضافة تنسيق إضافي هنا
        pass
    
    def run_all_scripts(self):
        """تشغيل جميع السكريبتات"""
        if not self.current_file_path:
            QMessageBox.warning(self, "تحذير", "يرجى استيراد ملف النص أولاً")
            return
        
        # عرض شريط التقدم
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # تعطيل الأزرار
        for btn in self.script_buttons:
            btn.setEnabled(False)
        
        # تشغيل جميع السكريبتات
        self.all_worker = AllScriptsWorker(self.runner)
        self.all_worker.finished.connect(self.on_all_scripts_finished)
        self.all_worker.start()
    
    def on_all_scripts_finished(self, results):
        """عند انتهاء تشغيل جميع السكريبتات"""
        # إخفاء شريط التقدم
        self.progress_bar.setVisible(False)
        
        # تفعيل الأزرار
        for btn in self.script_buttons:
            btn.setEnabled(True)
        
        if results:
            self.results_text.setPlainText(results)
        else:
            self.results_text.setPlainText("لا توجد نتائج")
    
    def export_results(self):
        """تصدير النتائج إلى ملف"""
        content = self.results_text.toPlainText()
        
        if not content.strip():
            QMessageBox.warning(self, "تحذير", "لا توجد نتائج للتصدير")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "حفظ النتائج",
            str(self.base_dir / "output" / "النتائج.txt"),
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            success, error = self.file_handler.save_results(content, Path(file_path).name)
            if success:
                QMessageBox.information(self, "نجح", f"تم حفظ النتائج في:\n{file_path}")
            else:
                QMessageBox.critical(self, "خطأ", f"فشل حفظ الملف:\n{error}")


def main():
    """تشغيل التطبيق"""
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # تعيين الخط الافتراضي - Sajjala Majala
    font = QFont("Sajjala Majala", 14)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

