from atlassian import Bitbucket
import logging
from typing import List


class Server:
    """
    Class that represents the BitBucket server.

    Has methods to perform queries on the server.
    """

    def __init__(self, url: str, user: str, password: str):
        """
        C'tor of Server.

        :param str url: URL of the BitBucket server
        :param str user: Login username
        :param str password: Login password or token
        """
        self.server_url = url
        self.user = user
        self.password = password
        self.api = Bitbucket(self.server_url, self.user, self.password)

    def project_list(self) -> List[str]:
        """
        Get the list of projects from the server.

        :return: List of project names
        """
        query = self.api.project_list()
        return query

    def pr_approved(self, project: str, repo: str, pr: int) -> bool:
        """
        Return True if at least one reviewer approved the pull request, otherwise False.

        :param: project Project ID of the repository
        :param: repo Repository slug of the pull request
        :param: pr Pull request ID
        :returns: True if one reviewer approved the pull request, otherwise False
        """
        query = self.api.get_pull_request(project, repo, pr)
        for reviewer in query["reviewers"]:
            if reviewer["approved"]:
                return True
        return False

    def open_pr_in_repo(
        self,
        project: str,
        repo: str,
        src_branch: str,
        dst_branch: str,
        title: str,
        desc: str,
        reviewers: str = None,
    ):
        """
        Open a new pull request in a repository.

        :param project: Project name
        :param repo: Repository name
        :param src_branch: Source branch name
        :param dst_branch: Destination branch name
        :param title: Title of the pull request
        :param desc: Description text of the pull request
        :param reviewers: UUIDs of reviewers (default None)
        """
        self.open_pr(
            project, repo, src_branch, project, repo, dst_branch, title, desc, reviewers
        )

    def open_pr(
        self,
        src_project: str,
        src_repo: str,
        src_branch: str,
        dst_project: str,
        dst_repo: str,
        dst_branch: str,
        title: str,
        desc: str,
        reviewers: str = None,
    ):
        """
        Open a new pull request.

        :param src_project: Source project name
        :param src_repo: Source repository name
        :param src_branch: Source branch name
        :param dst_project: Destination project name
        :param dst_repo: Destination repository name
        :param dst_branch: Destination branch name
        :param title: Title of the pull request
        :param desc: Description text of the pull request
        :param reviewers: UUIDs of reviewers (default None)
        """
        logging.info("Attempting to open a pull request:")
        logging.info(title)
        logging.info(desc)
        if self._confirm(
            "Open pull request "
            + src_project
            + "/"
            + src_repo
            + "/"
            + src_branch
            + "->"
            + dst_project
            + "/"
            + dst_repo
            + "/"
            + dst_branch
        ):
            self.api.open_pull_request(
                src_project,
                src_repo,
                dst_project,
                dst_repo,
                src_branch,
                dst_branch,
                title,
                desc,
                reviewers,
            )
            print("Success")
        else:
            print("Action aborted")

    @staticmethod
    def _confirm(question: str) -> bool:
        """Ask for user decision on question."""
        reply = str(input(question + " (y/n): ")).lower().strip()
        return reply[0] == "y"
