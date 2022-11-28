import tkinter as tk
from tkinter import ttk
from pyperclip import copy
from src.manage_files import *


class Window:
    """Main window of the application
    """

    def __init__(self, width: int = 500, height: int = 600):
        """Initialize the window

        Args:
            width (int, optional): Width of the window. Defaults to 500.
            height (int, optional): Height of the window. Defaults to 600.
        """
        self.root = tk.Tk()
        self.root.title("Quick Readme")
        self.root.iconbitmap("assets/icon.ico")
        self.width = width
        self.height = height
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

        # theme settings
        self.root.tk.call('source', 'theme/azure_dark.tcl')
        style = ttk.Style(self.root)
        style.theme_use('azure')

        self.directory = ""
        self.result = "test\n"

        self.generate_all()

        self.root.mainloop()

    def copy_text(self):
        """Copy the markdown content to the clipboard
        """
        copy(self.result)

    def download_file(self):
        """Download the markdown file
        """
        if self.directory == "":
            tk.messagebox.showerror('Quick Readme', 'Error: No directory selected')
        with open(self.directory + "/README.md", "w") as file:
            file.write(self.result)

    def open_edit_text_window(self):
        """Open the edit text window
        """
        edit_text_window = tk.Tk()
        edit_text_window.title("Edit Text")
        edit_text_window.iconbitmap("assets/icon.ico")
        edit_text_window.geometry(f"{self.width}x{self.height}")
        edit_text_window.configure(bg="#222222")

        tk.Grid.rowconfigure(edit_text_window,0,weight=1)
        tk.Grid.columnconfigure(edit_text_window,0,weight=1)

        def save_text_and_quit():
            self.result = text_box.get("1.0", "end-1c")
            edit_text_window.destroy()

        text_box = tk.Text(edit_text_window, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        text_box.insert(tk.END, self.result)
        text_box.grid(row=0, column=0, sticky="NSEW", padx=edit_text_window.winfo_width() * 0.03, pady=edit_text_window.winfo_height() * 0.03)

        edit_text_window.protocol("WM_DELETE_WINDOW", save_text_and_quit)
        edit_text_window.mainloop()

    def set_directory_path(self):
        """Set the directory path
        """ 
        self.directory = get_directory_path()
        if self.directory != "":
            self.button_select_directory.config(text=self.directory.split("/")[-1])


    def generate_top_infos(self):
        """Generate a button to edit text, and the directory input
        """
        button_edit_text = ttk.Button(self.root, text="Edit Text", command=self.open_edit_text_window)
        button_edit_text.place(x=5, y=5)

        self.directory_label = tk.Label(self.root, text="Directory :")
        self.directory_label.place(x=self.width * 0.45, y=10)

        self.button_select_directory = tk.Button(self.root, text="Select Directory", width=18, command=self.set_directory_path)
        self.button_select_directory.place(x=self.width * 0.45 + 70, y=8)

    def generate_main_section(self):
        print('generate_main_section: not implemented yet')
        pass

    def generate_separator(self):
        """Generate the separator between the main section and the buttons
        """
        separator = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        separator.place(x=self.width * 0.07, y=self.height - 70, relwidth=0.86)

    def generate_buttons(self):
        """Generate the buttons copy and download at the bottom of the window
        """
        button_copy = ttk.Button(self.root, text="📜     Copy Text", width=18, command=self.copy_text)
        button_copy.place(x=self.width * 0.5 - self.width * 0.04, anchor='ne', y=self.height - 50)

        button_download = ttk.Button(self.root, text="⬇️Download File", width=18, command=self.download_file)
        button_download.place(x=self.width * 0.5 + self.width * 0.04, y=self.height - 50)

    def generate_all(self):
        """Generate all the elements of the window
        """
        self.generate_top_infos()
        self.generate_main_section()
        self.generate_separator()
        self.generate_buttons()
