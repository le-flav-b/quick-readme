import tkinter.filedialog as dialog


def get_directory_path() -> str:
    return dialog.askdirectory(initialdir='d:/current_projects/')

def get_file_path() -> str:
    return dialog.askopenfilename(initialdir='d:/current_projects/')

def get_directory_name(directory_path: str) -> str:
    return directory_path.split('/')[-1]

def get_git_repo_name(directory_path: str) -> str:
    return get_directory_name(directory_path).replace('_', '-')

def get_project_name(directory_path: str) -> str:
    return get_directory_name(directory_path).replace('_', ' ').title()
