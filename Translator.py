from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from deep_translator import GoogleTranslator
import sys

# ---------- Constants / Palette ----------
PRIMARY = "#1a73e8"        # accent blue
TEXT_BLUE = "#0b5394"      # readable text on white
LIGHT_BG_TOP = "#e8f1fb"
LIGHT_BG_BOTTOM = "#cfe5ff"
CARD_BG = "rgba(255,255,255,0.88)"  # glassmorphism effect
BORDER = "#b3d1f5"         # soft light-blue border
SUBTEXT = "#5f6368"

# ---------- Worker thread for translation ----------
class TranslateThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text, target):
        super().__init__()
        self.text = text
        self.target = target

    def run(self):
        try:
            translated = GoogleTranslator(source="auto", target=self.target).translate(self.text)
            self.finished.emit(translated)
        except Exception as e:
            self.error.emit(str(e))


# ---------- Main Window ----------
class TranslatorWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setMinimumSize(980, 600)
        self.setWindowIcon(QtGui.QIcon())
        self.setStyleSheet("font-family: 'Helvetica Neue';")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(28, 20, 28, 18)
        layout.setSpacing(12)

        # ---------- Header ----------
        title_row = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("Translator")
        title.setStyleSheet(f"color: {PRIMARY}; font-weight: 700; font-size: 24px;")
        subtitle = QtWidgets.QLabel("")
        subtitle.setStyleSheet(f"color: {SUBTEXT}; font-size: 12px; margin-left: 8px;")
        title_row.addWidget(title)
        title_row.addWidget(subtitle)
        title_row.addStretch()
        layout.addLayout(title_row)

        # ---------- Content ----------
        content = QtWidgets.QHBoxLayout()
        content.setSpacing(20)

        # Left Input Card
        self.input_card = QtWidgets.QFrame()
        self._style_card(self.input_card)
        self.input_card.setMinimumWidth(400)
        in_layout = QtWidgets.QVBoxLayout(self.input_card)
        in_layout.setContentsMargins(16, 14, 16, 14)
        in_label = QtWidgets.QLabel("Enter text")
        in_label.setStyleSheet(f"color: {TEXT_BLUE}; font-weight: 600; font-size: 12px;")
        self.input_text = QtWidgets.QTextEdit()
        self._style_textedit(self.input_text)
        in_layout.addWidget(in_label)
        in_layout.addWidget(self.input_text)

        # Right Output Card
        self.output_card = QtWidgets.QFrame()
        self._style_card(self.output_card)
        self.output_card.setMinimumWidth(400)
        out_layout = QtWidgets.QVBoxLayout(self.output_card)
        out_layout.setContentsMargins(16, 14, 16, 14)
        out_label = QtWidgets.QLabel("Translation")
        out_label.setStyleSheet(f"color: {TEXT_BLUE}; font-weight: 600; font-size: 12px;")
        self.output_text = QtWidgets.QTextEdit()
        self.output_text.setReadOnly(True)
        self._style_textedit(self.output_text)
        out_layout.addWidget(out_label)
        out_layout.addWidget(self.output_text)

        # ---------- Center Controls ----------
        center_col = QtWidgets.QVBoxLayout()
        center_col.setSpacing(20)
        center_col.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        langs = ['english', 'french', 'german', 'spanish', 'hindi', 'italian',
                 'japanese', 'chinese', 'arabic', 'russian', 'portuguese']

        self.src_combo = QtWidgets.QComboBox()
        self.src_combo.addItems(["Auto Detect"] + langs)
        self._style_combo(self.src_combo)
        self.src_combo.setCurrentText("Auto Detect")

        self.dest_combo = QtWidgets.QComboBox()
        self.dest_combo.addItems(langs)
        self._style_combo(self.dest_combo)
        self.dest_combo.setCurrentText("english")

        self.swap_btn = QtWidgets.QPushButton("🔁")
        self.swap_btn.setFixedSize(52, 44)
        self.swap_btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        self.swap_btn.setStyleSheet(self.swap_button_style())
        self.swap_btn.clicked.connect(self.swap_languages)

        center_col.addWidget(self.src_combo)
        center_col.addWidget(self.swap_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_col.addWidget(self.dest_combo)

        content.addWidget(self.input_card)
        content.addLayout(center_col)
        content.addWidget(self.output_card)
        layout.addLayout(content)

        # ---------- Bottom Row ----------
        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.setSpacing(12)

        self.translate_btn = QtWidgets.QPushButton("Translate")
        self.translate_btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        self.translate_btn.setFixedSize(180, 48)
        self.translate_btn.setStyleSheet(self.translate_button_style())
        self.translate_btn.clicked.connect(self.on_translate)
        bottom_row.addWidget(self.translate_btn)

        self.status_label = QtWidgets.QLabel("Developed by Shabbir Hardwarewala")
        self.status_label.setStyleSheet(f"color: {SUBTEXT}; font-size: 11px; margin-left: 12px;")
        bottom_row.addWidget(self.status_label)
        bottom_row.addStretch()
        layout.addLayout(bottom_row)

        # ---------- Drop Shadows ----------
        for card in (self.input_card, self.output_card):
            shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=18, offset=QtCore.QPointF(0, 6))
            shadow.setColor(QtGui.QColor(199, 224, 255, 190))
            card.setGraphicsEffect(shadow)

        btn_shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=24, offset=QtCore.QPointF(0, 8))
        btn_shadow.setColor(QtGui.QColor(26, 115, 232, 160))
        self.translate_btn.setGraphicsEffect(btn_shadow)

    # ---------- Styles ----------
    def _style_card(self, widget):
        widget.setStyleSheet(f"""
            QFrame {{
                background: {CARD_BG};
                border: 1px solid {BORDER};
                border-radius: 12px;
            }}
        """)

    def _style_textedit(self, te):
        te.setStyleSheet(f"""
            QTextEdit {{
                background: rgba(255,255,255,0.96);
                color: {TEXT_BLUE};
                border: 1px solid {BORDER};
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
            }}
            QTextEdit:focus {{
                border: 1px solid {PRIMARY};
            }}
        """)

    def _style_combo(self, combo):
        combo.setFixedWidth(200)
        combo.setFixedHeight(42)
        combo.setFont(QtGui.QFont("Helvetica Neue", 11))
        combo.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        combo.setStyleSheet(f"""
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid {BORDER};
                border-radius: 10px;
                padding: 8px 14px;
                color: {TEXT_BLUE};
                font-weight: 500;
            }}
            QComboBox::drop-down {{
                border: 0px;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: url(data:image/svg+xml;utf8,
                    <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='{PRIMARY}'><path d='M4 6l4 4 4-4z'/></svg>);
                margin-right: 8px;
            }}
            QComboBox:hover {{
                background-color: rgba(245, 249, 255, 0.98);
                border: 1px solid {PRIMARY};
            }}
            QComboBox QAbstractItemView {{
                background-color: #ffffff;
                border: 1px solid {BORDER};
                selection-background-color: {PRIMARY};
                selection-color: white;
                border-radius: 8px;
                padding: 4px;
            }}
        """)

    def translate_button_style(self):
        return f"""
            QPushButton {{
                color: white;
                background: {PRIMARY};
                border-radius: 24px;
                font-weight: 700;
                font-size: 15px;
                border: none;
            }}
            QPushButton:hover {{
                background: #1565c0;
            }}
            QPushButton:pressed {{
                background: #0f4f9a;
            }}
        """

    def swap_button_style(self):
        return f"""
            QPushButton {{
                background: rgba(255,255,255,0.96);
                border: 1px solid {BORDER};
                color: {PRIMARY};
                border-radius: 10px;
                font-size: 16px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                color: #1565c0;
                background: rgba(210,227,252,0.85);
            }}
        """

    # ---------- Functional Logic ----------
    def swap_languages(self):
        s = self.src_combo.currentText()
        d = self.dest_combo.currentText()
        if s != "Auto Detect":
            self.src_combo.setCurrentText(d)
        self.dest_combo.setCurrentText(s if s != "Auto Detect" else self.dest_combo.currentText())

    def on_translate(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            self.status_label.setText("Please enter text to translate.")
            return
        target = self.dest_combo.currentText()
        if not target:
            self.status_label.setText("Please select a target language.")
            return

        self.translate_btn.setEnabled(False)
        self.status_label.setText("Translating...")
        self.thread = TranslateThread(text, target)
        self.thread.finished.connect(self.on_result)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def on_result(self, translated):
        self.output_text.setPlainText(translated)
        self.translate_btn.setEnabled(True)
        self.status_label.setText("Done — Powered by GoogleTranslator")

    def on_error(self, err):
        self.output_text.clear()
        self.translate_btn.setEnabled(True)
        self.status_label.setText(f"Error: {err}")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.rect()
        grad = QtGui.QLinearGradient(
            QtCore.QPointF(rect.topLeft()),
            QtCore.QPointF(rect.bottomLeft())
        )
        grad.setColorAt(0.0, QtGui.QColor(LIGHT_BG_TOP))
        grad.setColorAt(1.0, QtGui.QColor(LIGHT_BG_BOTTOM))
        painter.fillRect(rect, grad)


# ---------- Entry ----------
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Helvetica Neue", 10))
    w = TranslatorWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

