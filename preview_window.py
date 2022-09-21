import tkinter as tk
from markdown import markdown
from tkhtmlview import HTMLLabel
from markdown_converter import to_markdown

class PreviewWindow:
    
    def __init__(self, darkmode, sections):
        self.root = tk.Tk()
        self.root.geometry('720x1080')
        self.root.iconbitmap('icon.ico')
        self.root.title("Readme Preview")
        self.sections = sections
        self.html_label = HTMLLabel(self.root, html=self.to_html(), background='#202226' if darkmode else '#F8F8F8')
        
    def to_html(self):
        return markdown(to_markdown(self.sections))
