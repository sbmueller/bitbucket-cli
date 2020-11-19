from git import Repo
import os


class GitRepo:
    """Represents a git repository in the working directory."""

    def __init__(self):
        """C'tor."""
        self.repo = Repo(os.getcwd())

    def get_branch_name(self) -> str:
        """
        Return the current branch name.

        :return: Current branch name string.
        """
        return self.repo.active_branch.name

    def get_repo_name(self) -> str:
        """
        Return the current repository name if the URL follows the scheme
        [...]/project/repo.git.

        :return: Name of the repository on the origin remote
        """
        remote = self.repo.remote().url
        return remote.rsplit("/", 1)[-1][:-4]

    def get_remote_project(self) -> str:
        """
        Return name of the project on the origin remote, if the URL follows the
        scheme [...]/project/repo.git.

        :return: Name of the project on the origin remote
        """
        remote = self.repo.remote().url
        return remote.rsplit("/", 2)[-2]

    def get_last_commit_title(self) -> str:
        """
        Return the title (first line) of the last commit message in the current branch.

        :return: Commit title
        """
        return self.repo.commit("HEAD").message.splitlines()[0]

    def get_last_commit_desc(self) -> str:
        """
        Return the description (lines 2 ff.) of the last commit message in the current
        branch. Empty string of no description is available.

        :return: Commit description
        """
        commit_msg = self.repo.commit("HEAD").message.splitlines()[0]
        if len(commit_msg) > 1:
            return "\n".join(commit_msg[1:])
        return ""
