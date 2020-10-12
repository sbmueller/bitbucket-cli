from git import Repo
import os


class GitRepo:
    """
    Represents a git repository in the working directory.
    """

    def __init__(self):
        self.repo = Repo(os.getcwd())

    def get_branch_name(self):
        """
        Returns the name of the current branch.
        """
        return self.repo.active_branch().name

    def get_repo_name(self):
        """
        Returns the name of the repository on the remote, if the URL follows the scheme
        [...]/project/repo.git.
        """

    def get_remote_project(self):
        """
        Returns the name of the project on the remote, if the URL follows the scheme
        [...]/project/repo.git.
        """

