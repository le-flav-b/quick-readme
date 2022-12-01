import tkinter as tk
from tkinter import ttk
from pyperclip import copy as pycopy
from src.littles_functions import *
from src.eval_markdown import eval_markdown
from io import open as iopen

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

        self.result = ""

        self.sections = ["Base (obligatory) : ", "Description : ", "Screenshots : ", "List of Features : ", "List of Changes in Progress : ", "List of co-Authors : ", "Installation Instructions : ", "Usage Instructions : ", "Other Sections : "]
        self.infos = {
            'directory': "",
            'logo': "",
            'screenshots': "",
            'emoji': "",
            'subtitle': "",
            'description': "",
            'features': "",
            'changes': "",
            'authors': "",
            'installation': "",
            'usage': "",
            'tree': 1,
            'feedback': 0,
            'contributing': 0,
            'reachme': 1
        }
        self.obligatory = ['directory', 'logo', 'emoji', 'subtitle']

        self.generate_all()

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def close(self) -> None:
        destroy = True
        self.complete_infos()
        enough = True
        for info in self.infos:
            if info in ['tree', 'feedback', 'contributing', 'reachme']:
                continue
            if self.infos[info] == "":
                if info in self.obligatory:
                    enough = False
            else:
                destroy = False
        if not destroy and (not enough or self.result != eval_markdown(self.infos)):
            yes_no_cancel = tk.messagebox.askyesnocancel('Quick Readme', 'You are about to close the application without saving the changes. Do you want to download the README.md ?')
            if yes_no_cancel:
                self.download_file()
                if self.infos['directory'] == "" or self.result is None:
                    yes_no_cancel = None
            if yes_no_cancel is not None:
                destroy = True
        else:
            destroy = True
        if destroy:
            if self.info_other[2].get():
                tk.messagebox.showinfo('Quick Readme', "Don't forget to create the contributing.md file !")
            self.root.destroy()

    def complete_infos(self) -> None:
        """Complete the infos dictionary with the text of the entry
        """
        self.infos['emoji'] = self.info_emoji.get("1.0", "end-1c")
        self.infos['subtitle'] = self.info_subtitle.get("1.0", "end-1c")
        self.infos['description'] = self.info_description.get("1.0", "end-1c")
        self.infos['features'] = self.info_features.get("1.0", "end-1c")
        self.infos['changes'] = self.info_changes.get("1.0", "end-1c")
        self.infos['authors'] = self.info_authors.get("1.0", "end-1c")
        self.infos['installation'] = self.info_installation.get("1.0", "end-1c")
        self.infos['usage'] = self.info_usage.get("1.0", "end-1c")
        self.infos['tree'] = self.info_other[0].get()
        self.infos['feedback'] = self.info_other[1].get()
        self.infos['contributing'] = self.info_other[2].get()
        self.infos['reachme'] = self.info_other[3].get()

    def eval_markdown_before(self) -> int:
        """Evaluate the markdown before copying or downloading

        Returns:
            int: 1 if the markdown is ready to be copy or download, 0 if not
        """
        self.complete_infos()
        for info in self.obligatory:
            if self.infos[info] == "":
                tk.messagebox.showerror("Quick Readme", f"You must fill the {info} section.")
                self.result = ""
                return 0
        self.result = eval_markdown(self.infos)
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
            with iopen(self.infos['directory'] + "/README.md", "w", encoding="utf-8") as file:
                file.write(self.result)

    def open_edit_text_window(self) -> None:
        """Open the edit text window
        """
        tk.messagebox.showwarning("Quick Readme", "If you change something from the edit window it will not be taken into account in th main window.")
        self.complete_infos()
        if not self.eval_markdown_before():
            return
        edit_text_window = tk.Tk()
        edit_text_window.title("Edit Text")
        edit_text_window.iconbitmap("assets/icon.ico")
        edit_text_window.geometry(f"{self.width}x{self.height}")
        edit_text_window.minsize(450, 135) #########""
        edit_text_window.configure(bg="#222222")

        tk.Grid.rowconfigure(edit_text_window,0,weight=1)
        tk.Grid.columnconfigure(edit_text_window,0,weight=1)

        text_box = tk.Text(edit_text_window, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        text_box.insert(tk.END, self.result)
        edit_text_window.update()
        #text_box.place(relwidth=0.96, relx=0.02, height=edit_text_window.winfo_height() - 70, y=edit_text_window.winfo_height() * 0.02)
        text_box.grid(row=0, column=0, sticky="NSEW", padx=edit_text_window.winfo_width() * 0.02, pady=edit_text_window.winfo_height() * 0.02)

        def my_copy():
            pycopy(text_box.get("1.0", "end-1c"))
        
        def my_save():
            with iopen(self.infos['directory'] + "/README.md", "w", encoding="utf-8") as file:
                file.write(text_box.get("1.0", "end-1c"))

        separator = ttk.Separator(edit_text_window, orient=tk.HORIZONTAL)
        #separator.place(x=edit_text_window.winfo_width() * 0.07, y=edit_text_window.winfo_height() - 50, relwidth=0.86)
        separator.grid(row=1, column=0, sticky="EW", padx=edit_text_window.winfo_width() * 0.07, pady=0)

        button_copy = ttk.Button(edit_text_window, text="📜     Copy Text", width=18, command=my_copy)
        #button_copy.place(x=edit_text_window.winfo_width() * 0.5 - edit_text_window.winfo_width() * 0.04, anchor='ne', y=edit_text_window.winfo_height() - 35)
        button_copy.grid(row=2, column=0, sticky="W", padx=edit_text_window.winfo_width() * 0.2, pady=edit_text_window.winfo_height() * 0.02)

        button_download = ttk.Button(edit_text_window, text="⬇️Download File", width=18, command=my_save)
        #button_download.place(x=edit_text_window.winfo_width() * 0.5 + edit_text_window.winfo_width() * 0.04, y=edit_text_window.winfo_height() - 35)
        button_download.grid(row=2, column=0, sticky="E", padx=edit_text_window.winfo_width() * 0.2, pady=edit_text_window.winfo_height() * 0.02)

        def save_text_and_quit():
            """Save the text and quit the window
            """
            self.result = text_box.get("1.0", "end-1c")
            edit_text_window.destroy()

        edit_text_window.protocol("WM_DELETE_WINDOW", save_text_and_quit)
        edit_text_window.mainloop()

    def set_directory_path(self) -> None:
        """Set the directory path
        """ 
        self.infos['directory'] = get_directory_path()
        if self.infos['directory'] != "":
            self.button_select_directory.config(text=get_directory_name(self.infos['directory']))
    
    def set_file_path(self, info: str) -> None:
        """Set the file path
        """ 
        self.infos[info] = get_file_path(self.infos['directory'])
        if self.infos[info] != "":
            if info == 'logo':
                self.info_logo.config(text=get_file_name(self.infos[info]))
            else:
                self.info_screenshots.config(text=get_file_name(self.infos[info]))

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

        self.main_section = tk.LabelFrame(self.root, bg="#3B3B3B")
        self.main_section.place(x=self.width * 0.04, y=45, width=self.width * 0.92, height=self.height - 135)

        self.main_section_canvas = tk.Canvas(self.main_section)
        self.main_section_canvas.pack(side=tk.LEFT, fill="both", expand=1)

        yscrollbar = ttk.Scrollbar(self.main_section, orient="vertical", command=self.main_section_canvas.yview)
        yscrollbar.pack(side=tk.RIGHT, fill="y")

        self.main_section_canvas.configure(yscrollcommand=yscrollbar.set)
        self.main_section_canvas.bind('<Configure>', lambda e: self.main_section_canvas.configure(scrollregion = self.main_section_canvas.bbox('all')))
        self.main_frame = tk.Frame(self.main_section_canvas)
        self.main_section_canvas.create_window((0,0), window=self.main_frame, anchor="nw")

        self.labels_frames = [tk.LabelFrame(self.main_frame, text=section, bg="#3B3B3B", fg="#f2f2f2", font=("Arial", 12)) for section in self.sections]
        [label.pack(fill="both", padx=10, pady=10, ipadx=10, ipady=10) for label in self.labels_frames]
        tk.Button(self.main_frame).pack(pady=714) # wtf
        
        ######  Base (obligatory) :  ######
        tk.Label(self.labels_frames[0], text="Choose a Logo :").grid(row=0, column=0, padx=5, pady=8)
        self.info_logo = tk.Button(self.labels_frames[0], text="Select Logo", width=18, command=lambda: self.set_file_path('logo'))
        self.info_logo.grid(row=0, column=1, padx=5, pady=8)

        tk.Label(self.labels_frames[0], text="Choose an Emoji :").grid(row=1, column=0, padx=5, pady=8)
        self.info_emoji = tk.Text(self.labels_frames[0], width=3, height=1, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        self.info_emoji.grid(row=1, column=1, padx=5, pady=8)
        
        tk.Label(self.labels_frames[0], text="Choose a Subtitle :").grid(row=2, column=0, padx=5, pady=8)
        self.info_subtitle = tk.Text(self.labels_frames[0], width=30, height=2, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        self.info_subtitle.grid(row=2, column=1, padx=5, pady=8)

        ######  Description :  ######
        self.info_description = tk.Text(self.labels_frames[1], width=42, height=8, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        self.info_description.grid(row=0, column=0, padx=5, pady=8)

        ######  Screenshots :  ######
        tk.Label(self.labels_frames[2], text="Choose some Screenshots, a Gif, a Graph... :").grid(row=0, column=0, padx=5, pady=8)
        self.info_screenshots = tk.Button(self.labels_frames[2], text="Select Image", width=18, command=lambda: self.set_file_path('screenshots'))
        self.info_screenshots.grid(row=0, column=1, padx=5, pady=8)
        
        ######  List of Features :  ######
        self.info_features = tk.Text(self.labels_frames[3], width=42, height=8, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        self.info_features.grid(row=0, column=0, padx=5, pady=8)
        
        ######  List of Changes in Progress :  ######
        self.info_changes = tk.Text(self.labels_frames[4], width=42, height=8, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        self.info_changes.grid(row=0, column=0, padx=5, pady=8)
        
        ######  List of co-Authors :  ######
        self.info_authors = tk.Text(self.labels_frames[5], width=42, height=8, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        self.info_authors.grid(row=0, column=0, padx=5, pady=8)
        
        ######  Installation Instructions :  ######
        self.info_installation = tk.Text(self.labels_frames[6], width=42, height=8, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        self.info_installation.grid(row=0, column=0, padx=5, pady=8)
        
        ######  Usage Instructions :  ######
        self.info_usage = tk.Text(self.labels_frames[7], width=42, height=8, bg="#2a2a2a", fg="#f2f2f2", font=("Arial", 12))
        self.info_usage.grid(row=0, column=0, padx=5, pady=8)
        
        ######  Other Sections :  ######
        self.info_other = [tk.IntVar() for _ in range(4)]
        tk.Label(self.labels_frames[8], text=" "*25, bg="#3B3B3B").grid(row=0, column=0, padx=5, pady=8)
        self.info_tree = tk.Checkbutton(self.labels_frames[8], text="Tree", variable=self.info_other[0], onvalue=1, offvalue=0, selectcolor="#2a2a2a", bg="#3B3B3B", fg="#f2f2f2", font=("Arial", 12))
        self.info_tree.grid(row=0, column=1, padx=5, pady=8)
        self.info_tree.select()

        self.info_feedback = tk.Checkbutton(self.labels_frames[8], text="Feedback", variable=self.info_other[1], onvalue=1, offvalue=0, selectcolor="#2a2a2a", bg="#3B3B3B", fg="#f2f2f2", font=("Arial", 12))
        self.info_feedback.grid(row=0, column=2, padx=5, pady=8)

        self.info_contributing = tk.Checkbutton(self.labels_frames[8], text="Contributing", variable=self.info_other[2], onvalue=1, offvalue=0, selectcolor="#2a2a2a", bg="#3B3B3B", fg="#f2f2f2", font=("Arial", 12))
        self.info_contributing.grid(row=1, column=1, padx=5, pady=8)

        self.info_reach_me = tk.Checkbutton(self.labels_frames[8], text="Reach Me", variable=self.info_other[3], onvalue=1, offvalue=0, selectcolor="#2a2a2a", bg="#3B3B3B", fg="#f2f2f2", font=("Arial", 12))
        self.info_reach_me.grid(row=1, column=2, padx=5, pady=8)
        self.info_reach_me.select()

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
