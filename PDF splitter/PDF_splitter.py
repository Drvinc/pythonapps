#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
                               QLineEdit, QPushButton, QFileDialog, QWidget)
from PySide6.QtCore import Qt
import pypdf

class PDFExtractor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Page Extractor")
        self.setGeometry(100, 100, 400, 250)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Drag and Drop a PDF file here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setAcceptDrops(True)
        self.label.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")
        self.layout.addWidget(self.label)

        self.page_count_label = QLabel("")
        self.page_count_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.page_count_label)

        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Enter pages to keep (e.g., 1, 3-5, 7)")
        self.layout.addWidget(self.page_input)

        self.save_button = QPushButton("Save Selected Pages")
        self.save_button.clicked.connect(self.save_pages)
        self.layout.addWidget(self.save_button)

        self.pdf_path = None
        self.total_pages = 0

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].scheme() == 'file':
            self.pdf_path = urls[0].toLocalFile()
            self.label.setText(f"Loaded PDF: {self.pdf_path}")
            self.display_page_count()

    def display_page_count(self):
        try:
            reader = pypdf.PdfReader(self.pdf_path)
            self.total_pages = len(reader.pages)
            self.page_count_label.setText(f"Total Pages: {self.total_pages}")
        except Exception as e:
            self.page_count_label.setText(f"Error reading PDF: {e}")

    def parse_pages(self, pages_text):
        pages = []
        for part in pages_text.split(','):
            if '-' in part:
                start, end = part.split('-')
                pages.extend(range(int(start) - 1, int(end)))
            else:
                pages.append(int(part) - 1)
        return pages

    def save_pages(self):
        if not self.pdf_path:
            self.label.setText("Please drag and drop a PDF file first.")
            return

        pages_text = self.page_input.text()
        if not pages_text:
            self.label.setText("Please enter pages to keep.")
            return

        try:
            pages_to_keep = self.parse_pages(pages_text)
        except ValueError:
            self.label.setText("Invalid page input.")
            return

        try:
            reader = pypdf.PdfReader(self.pdf_path)
            writer = pypdf.PdfWriter()

            for page_num in pages_to_keep:
                if 0 <= page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
                else:
                    self.label.setText("Invalid page range.")
                    return

            save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
            if save_path:
                with open(save_path, "wb") as output_pdf:
                    writer.write(output_pdf)
                new_total_pages = len(pages_to_keep)
                self.page_count_label.setText(f"Total Pages: {self.total_pages} -> {new_total_pages}")
                self.label.setText(f"Selected pages saved to {save_path}")
        except Exception as e:
            self.label.setText(f"Error processing PDF: {e}")

def main():
    app = QApplication(sys.argv)
    window = PDFExtractor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

