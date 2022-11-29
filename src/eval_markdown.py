from src.littles_functions import *
from seedir import seedir

def eval_markdown(infos: dict) -> str:
    """Evaluate the markdown content

    Args:
        window (Window): The main window

    Returns:
        str: The markdown content
    """
    with open('sections/base.txt', 'r') as text:
        result = text.read()
    for section, content in infos.items():
        if section not in ['directory', 'logo', 'emoji', 'subtitle'] and content:
            with open(f'sections/{section}.txt', 'r') as text:
                result += text.read()

    return result.format(
        project_name=get_project_name(infos['directory']),
        repo_git=get_git_repo_name(infos['directory']),
        logo=remove_start_of_path(infos['directory'], infos['logo']),
        emoji=infos['emoji'],
        subtitle=infos['subtitle'],
        description=infos['description'],
        screenshots=remove_start_of_path(infos['directory'], infos['screenshots']),
        features=to_list(infos['features']),
        changes=to_list(infos['changes']),
        authors=to_list(infos['authors']),
        tree=seedir(infos['directory'], style='emoji', exclude_folders=['.git'], printout=False).replace('/\n', '\n'),
        installation=infos['installation'],
        usage=infos['usage']
    )
