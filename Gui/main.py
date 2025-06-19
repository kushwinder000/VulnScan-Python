import sys
import os
import importlib
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QLabel, QMessageBox, QFileDialog,
    QProgressBar, QScrollArea, QFrame, QSizePolicy, QToolButton,
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QSize, QEasingCurve, QPropertyAnimation
from PyQt6.QtGui import QFont, QMovie, QIcon

from report_generator import save_as_txt, generate_pdf_report


class ScannerThread(QThread):
    output_signal = pyqtSignal(str, str)  # module_name, message
    progress_signal = pyqtSignal(int)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        modules_dir = 'modules'
        files = [f for f in os.listdir(modules_dir) if f.endswith(".py") and not f.startswith("__")]
        total = len(files)

        self.output_signal.emit("System", f"🔍 Starting scan on: {self.url}")

        for i, file in enumerate(files, 1):
            module_name = file[:-3]
            full_module = f"modules.{module_name}"

            self.output_signal.emit(module_name, f"📦 Running module: {module_name}")
            try:
                mod = importlib.import_module(full_module)
                mod.run(self.url, lambda msg: self.output_signal.emit(module_name, msg))
                self.output_signal.emit(module_name, f"✅ Finished: {module_name}")
            except Exception as e:
                self.output_signal.emit(module_name, f"❌ Error in {module_name}: {e}")

            progress = int((i / total) * 100)
            self.progress_signal.emit(progress)

        self.output_signal.emit("System", "🎯 Scan complete!")


class ExpandableModuleCard(QFrame):
    def __init__(self, module_name):
        super().__init__()
        self.module_name = module_name
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #121212;
                border-radius: 10px;
                border: 2px solid #00ffd5;
                margin-bottom: 12px;
                box-shadow: 0 0 10px #00ffd5;
            }
        """)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(4)

        # Header with toggle button
        self.header = QHBoxLayout()
        self.title_label = QLabel(f"📦 {module_name}")
        self.title_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #00ffd5;")
        self.header.addWidget(self.title_label)

        self.toggle_button = QToolButton()
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.setStyleSheet("""
            QToolButton {
                border: none;
                color: #00ffd5;
                font-size: 18px;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_content)
        self.header.addWidget(self.toggle_button)

        self.main_layout.addLayout(self.header)

        # Content area
        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)
        self.content_area.setFont(QFont("Consolas", 11))
        self.content_area.setStyleSheet("""
            QTextEdit {
                background-color: #222;
                color: #dcdcdc;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.content_area.setFixedHeight(160)
        self.main_layout.addWidget(self.content_area)

    def append_text(self, text):
        self.content_area.append(text)

    def toggle_content(self):
        if self.toggle_button.isChecked():
            self.content_area.show()
            self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
        else:
            self.content_area.hide()
            self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)


class VulnerabilityScannerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛡️ VulnScan - Website Vulnerability Scanner")
        self.setMinimumSize(1100, 720)

        # Gradient background for main window
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f2027, stop:0.5 #203a43, stop:1 #2c5364);
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("🛡️ VulnScan")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("""
            color: #00ffd5;
            text-shadow: 0 0 8px #00ffd5;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Input and button
        form_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("🔗 Enter website URL (e.g., https://example.com)")
        self.url_input.setFont(QFont("Segoe UI", 14))
        self.url_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                padding: 12px;
                border-radius: 10px;
                border: 2px solid #00ffd5;
            }
            QLineEdit:focus {
                border-color: #0ff;
                background-color: #252525;
            }
        """)
        self.url_input.returnPressed.connect(self.start_scan)

        self.scan_button = QPushButton("🚀 Start Scan")
        self.scan_button.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.scan_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_button.setStyleSheet("""
            QPushButton {
                background-color: #00ffd5;
                color: #000;
                padding: 14px 28px;
                border-radius: 12px;
                font-weight: bold;
                box-shadow: 0 0 10px #00ffd5;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #00bfae;
            }
            QPushButton:pressed {
                background-color: #008c7e;
            }
        """)
        self.scan_button.clicked.connect(self.start_scan)

        form_layout.addWidget(self.url_input)
        form_layout.addWidget(self.scan_button)
        main_layout.addLayout(form_layout)

        # Progress bar with glow effect
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00ffd5;
                border-radius: 12px;
                text-align: center;
                color: #00ffd5;
                background-color: #111;
                height: 28px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #00ffd5;
                border-radius: 12px;
                box-shadow: 0 0 15px #00ffd5;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Scroll area for modules
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_area.setWidget(scroll_content)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(self.scroll_area)

        # Export buttons
        export_layout = QHBoxLayout()
        self.save_txt_btn = QPushButton("💾 Save as TXT")
        self.save_txt_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #00ffd5;
                border: 2px solid #00ffd5;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ffd5;
                color: #000;
            }
        """)
        self.save_txt_btn.clicked.connect(self.save_as_txt)

        self.save_pdf_btn = QPushButton("📄 Generate PDF Report")
        self.save_pdf_btn.setStyleSheet(self.save_txt_btn.styleSheet())
        self.save_pdf_btn.clicked.connect(self.save_as_pdf)

        export_layout.addWidget(self.save_txt_btn)
        export_layout.addWidget(self.save_pdf_btn)
        main_layout.addLayout(export_layout)

        self.central_widget.setLayout(main_layout)

        self.module_cards = {}

        # Loading spinner GIF for scanning status
        self.spinner_label = QLabel()
        self.spinner_movie = QMovie("../../PythonProject/gui/spinner.gif")  # Add a spinner.gif in the same directory or use your own path
        self.spinner_label.setMovie(self.spinner_movie)
        self.spinner_label.setFixedSize(48, 48)
        self.spinner_label.setVisible(False)
        export_layout.addWidget(self.spinner_label)

    def start_scan(self):
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a URL to scan.")
            return

        if not url.startswith("http"):
            url = "http://" + url

        # Clear previous results
        self.module_cards.clear()
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.progress_bar.setValue(0)
        self.spinner_label.setVisible(True)
        self.spinner_movie.start()

        self.thread = ScannerThread(url)
        self.thread.output_signal.connect(self.handle_module_output)
        self.thread.progress_signal.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.scan_finished)
        self.thread.start()

    def handle_module_output(self, module_name, message):
        if module_name not in self.module_cards:
            card = ExpandableModuleCard(module_name)
            self.module_cards[module_name] = card
            self.scroll_layout.addWidget(card)
        else:
            card = self.module_cards[module_name]

        card.append_text(message)

    def save_as_txt(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Report as TXT", "", "Text Files (*.txt)")
        if filename:
            content = self.compile_report()
            save_as_txt(filename, content)

    def save_as_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Report as PDF", "", "PDF Files (*.pdf)")
        if filename:
            url = self.url_input.text().strip()
            content = self.compile_report()
            generate_pdf_report(filename, url, content)

    def compile_report(self):
        report = []
        for module_name, card in self.module_cards.items():
            report.append(f"--- Module: {module_name} ---\n")
            report.append(card.content_area.toPlainText())
            report.append("\n\n")
        return "\n".join(report)

    def scan_finished(self):
        self.spinner_movie.stop()
        self.spinner_label.setVisible(False)
        QMessageBox.information(self, "Scan Complete", "✅ Website scanning is complete!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VulnerabilityScannerGUI()
    window.show()
    sys.exit(app.exec())
