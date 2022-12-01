from src.littles_functions import *
from seedir import seedir

def eval_markdown(infos: dict) -> str:
    """Evaluate the markdown content

    Args:
        window (Window): The main window

    Returns:
        str: The markdown content
    """
    sections_links = {
        'features': 'Features',
        'changes': 'Changes In Progress',
        'authors': 'Co-Authors',
        'tree': 'Project Tree',
        'installation': 'Installation',
        'usage': 'Usage',
        'feedback' : 'A Feedback ?',
        'contributing': 'Contributing'
    }
    with open('sections/base.txt', 'r') as text:
        result = text.read()
    list_links = []
    for section_link, section_name in sections_links.items():
        if infos[section_link]:
            list_links.append('    <a href="#{}"=>{}</a>'.format(section_name.lower().replace(' ', '-').replace('?', ''), section_name))
    if len(list_links):
        with open('sections/links.txt', 'r') as text:
            result += text.read().format(links=' ·\n    '.join(list_links))
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
        description=infos['description'].replace('\n\n', '\n<br><br>\n').replace('•', '-'),
        screenshots=remove_start_of_path(infos['directory'], infos['screenshots']),
        features=to_list(infos['features']).replace('\n\n', '\n<br><br>\n'),
        changes=to_list(infos['changes']).replace('\n\n', '\n<br><br>\n'),
        authors=to_list(infos['authors']).replace('\n\n', '\n<br><br>\n'),
        tree=seedir(infos['directory'], style='emoji', exclude_folders=['.git'], printout=False).replace('/\n', '\n').replace('\n', '<br>\n'),
        installation=infos['installation'].replace('\n\n', '\n<br><br>\n').replace('•', '-'),
        usage=infos['usage'].replace('\n\n', '\n<br><br>\n').replace('•', '-')
    ).replace('Â', '')
