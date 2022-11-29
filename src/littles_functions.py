import tkinter.filedialog as dialog


def get_directory_path() -> str:
    return dialog.askdirectory(initialdir='d:/current_projects/')

def get_file_path(directory: str) -> str:
    return dialog.askopenfilename(initialdir=directory if directory != "" else 'd:/current_projects/')

def get_file_name(file_path: str) -> str:
    return file_path.split('/')[-1]

def get_directory_name(directory_path: str) -> str:
    return directory_path.split('/')[-1]

def get_git_repo_name(directory_path: str) -> str:
    return get_directory_name(directory_path).replace('_', '-')

def get_project_name(directory_path: str) -> str:
    return get_directory_name(directory_path).replace('_', ' ').title()

def to_list(string: str) -> str:
    return "* " + "\n* ".join(string.split())

def remove_start_of_path(directory: str, path: str) -> str:
    return path.split(get_directory_name(directory))[-1][1:]
