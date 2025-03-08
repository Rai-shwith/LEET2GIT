from github import InputGitTreeElement, Repository
from scripts.logging_config import logger

async def batch_upload_files(repo: Repository.Repository, file_structure: dict, commit_message: str = "Automated upload: User's LeetCode solutions added in bulk"):
    """
    Upload or update multiple files in a single commit.
    
    Args:
        repo: The repository object.
        file_structure: A dictionary representing files and their content. 
                        Example: {"path/to/file1.txt": "Content of file1", "path/to/file2.txt": "Content of file2"}
        commit_message: The commit message.
    """
    logger.info("Starting batch upload...")

    # Get the latest commit SHA of the default branch (e.g., main)
    ref = repo.get_git_ref("heads/main")
    latest_commit_sha = ref.object.sha
    logger.info(f"Latest commit SHA: {latest_commit_sha}")

    # Get the base tree object
    base_commit = repo.get_git_commit(latest_commit_sha)
    base_tree = base_commit.tree
    print("Base tree SHA: ", base_tree.sha)

    # Create tree items
    tree_items = []
    for path, content in file_structure.items():
        # Create an InputGitTreeElement for each file
        blob = repo.create_git_blob(content, "utf-8")
        tree_item = InputGitTreeElement(
            path=path,
            mode="100644",
            type="blob",
            sha=blob.sha
        )
        tree_items.append(tree_item)

    # Create a new tree
    new_tree = repo.create_git_tree(tree=tree_items, base_tree=base_tree)
    print("New tree SHA: ", new_tree.sha)

    # Create a new commit
    parent_commit = repo.get_git_commit(latest_commit_sha)
    new_commit = repo.create_git_commit(commit_message, new_tree, [parent_commit])

    # Update the reference to point to the new commit
    ref.edit(new_commit.sha)
    logger.info("Batch upload completed with a single commit!")