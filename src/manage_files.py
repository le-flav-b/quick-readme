import tkinter.filedialog as dialog


def get_directory_path():
    return dialog.askdirectory(initialdir='d:/current_projects/')

def get_file_path():
    return dialog.askopenfilename(initialdir='d:/current_projects/')