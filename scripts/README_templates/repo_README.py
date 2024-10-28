def get_repo_readme(readme_content : str,user_name: str,repo_name : str,folder_name : str,topic_tags:list[dict]):
    """
    This function will return a readme file with the given topic tags
    """
    for tag in topic_tags:
        # Search for the location where the tag is located
        index = readme_content.find(f"## {tag.get('name')}") 
        entry =  f"| [{folder_name}](https://github.com/{user_name}/{repo_name}/tree/master/{folder_name}) |\n"
        if index == -1: # If tag is not present in the readme content
            end_position = readme_content.find("<!---LeetCode Topics End-->")
            readme_content = readme_content[:end_position] + f"## {tag.get('name')}\n" + f"|  |\n| ------- |\n" + entry + readme_content[end_position:]
        elif (readme_content.find(entry) == -1): # If the entry is not present in the tag
            position = index + len(f"## {tag.get('name')}") + 18
            readme_content = readme_content[:position] + entry + readme_content[position:]
        return readme_content 
