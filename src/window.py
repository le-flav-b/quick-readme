import tkinter as tk
from tkinter import ttk
from pyperclip import copy as pycopy
from src.littles_functions import *
from src.eval_markdown import eval_markdown


class Window:
    """Main window of the application
    """

    def __init__(self, width: int = 500, height: int = 600) -> None:
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
        self.result = ""
        self.last_result = ""

        self.generate_all()

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def close(self) -> None:
        destroy = False
        if self.last_result != self.result:
            yes_no_cancel = tk.messagebox.askyesnocancel('Quick Readme', 'You are about to close the application without saving the changes. Do you want to download the README.md ?')
            if yes_no_cancel:
                self.download_file()
                if self.directory == "" or self.result is None:
                    yes_no_cancel = None
            if yes_no_cancel is not None:
                destroy = True
        else:
            destroy = True
        if destroy:
            # if contributing:  #TODO add a contributing condition
            #     tk.messagebox.showinfo('Quick Readme', "Don't forget to create the contributing.md file !")
            self.root.destroy()

    def eval_markdown_before(self) -> int:
        """Evaluate the markdown before copying or downloading

        Returns:
            int: 1 if the markdown is ready to be copy or download, 0 if not
        """
        if self.directory == "":
            tk.messagebox.showerror('Quick Readme', 'Error: No directory selected')
            return 0
        self.result = eval_markdown(self)
        if self.result is None:
            tk.messagebox.showerror("Quick Readme", "An error occurred !")
            return 0
        self.last_result = self.result
        return 1

    def copy_text(self) -> None:
        """Copy the markdown content to the clipboard
        """
        if self.eval_markdown_before():
            pycopy(self.result)

    def download_file(self) -> None:
        """Download the markdown file
        """
        if self.eval_markdown_before():
            with open(self.directory + "/README.md", "w") as file:
                file.write(self.result)

    def open_edit_text_window(self) -> None:
        """Open the edit text window
        """
        tk.messagebox.showwarning("Quick Readme", "Close the edit window will save modifications but only if you don't do other modifications by the interface after that.")

        self.result = eval_markdown(self)
        edit_text_window = tk.Tk()
        edit_text_window.title("Edit Text")
        edit_text_window.iconbitmap("assets/icon.ico")
        edit_text_window.geometry(f"{self.width}x{self.height}")
        edit_text_window.configure(bg="#222222")

        tk.Grid.rowconfigure(edit_text_window,0,weight=1)
        tk.Grid.columnconfigure(edit_text_window,0,weight=1)

        def save_text_and_quit() -> str:
            """Save the text and quit the window
            """
            self.result = text_box.get("1.0", "end-1c")
            self.last_result = self.result
            edit_text_window.destroy()

        text_box = tk.Text(edit_text_window, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        text_box.insert(tk.END, self.result)
        text_box.grid(row=0, column=0, sticky="NSEW", padx=edit_text_window.winfo_width() * 0.03, pady=edit_text_window.winfo_height() * 0.03)

        edit_text_window.protocol("WM_DELETE_WINDOW", save_text_and_quit)
        edit_text_window.mainloop()

    def set_directory_path(self) -> None:
        """Set the directory path
        """ 
        self.directory = get_directory_path()
        if self.directory != "":
            self.button_select_directory.config(text=get_directory_name(self.directory))


    def generate_top_infos(self) -> None:
        """Generate a button to edit text, and the directory input
        """
        button_edit_text = ttk.Button(self.root, text="Edit Text", command=self.open_edit_text_window)
        button_edit_text.place(x=5, y=5)

        self.directory_label = tk.Label(self.root, text="Directory :")
        self.directory_label.place(x=self.width * 0.45, y=10)

        self.button_select_directory = tk.Button(self.root, text="Select Directory", width=18, command=self.set_directory_path)
        self.button_select_directory.place(x=self.width * 0.45 + 70, y=8)

    def generate_main_section(self) -> None:
        """Generate the main section of the window, with the multiples sections that does the readme
        """
        self.main_section = tk.Frame(self.root, bg="#3B3B3B", width=self.width * 0.92, height=self.height - 135)
        self.main_section.place(x=self.width * 0.04, y=45)

        #TODO make the scrollable main section

    def generate_separator(self) -> None:
        """Generate the separator between the main section and the buttons
        """
        separator = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        separator.place(x=self.width * 0.07, y=self.height - 70, relwidth=0.86)

    def generate_buttons(self) -> None:
        """Generate the buttons copy and download at the bottom of the window
        """
        button_copy = ttk.Button(self.root, text="📜     Copy Text", width=18, command=self.copy_text)
        button_copy.place(x=self.width * 0.5 - self.width * 0.04, anchor='ne', y=self.height - 50)

        button_download = ttk.Button(self.root, text="⬇️Download File", width=18, command=self.download_file)
        button_download.place(x=self.width * 0.5 + self.width * 0.04, y=self.height - 50)

    def generate_all(self) -> None:
        """Generate all the elements of the window
        """
        self.generate_top_infos()
        self.generate_main_section()
        self.generate_separator()
        self.generate_buttons()
