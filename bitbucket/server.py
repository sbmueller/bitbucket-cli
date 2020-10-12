from atlassian import Bitbucket


class Server:
    """
    Class that represents the BitBucket server. Has methods to perform queries on the server.
    """

    def __init__(self, url, user, password):
        """
        C'tor of Server.

        :param: url URL of the BitBucket server
        :param: user Login username
        :param: password Login password or token
        """
        self.server_url = url
        self.user = user
        self.password = password
        self.api = Bitbucket(self.server_url, self.user, self.password)

    def project_list(self):
        """
        Gets the list of projects from the server.

        :returns: List of project names
        """
        query = self.api.project_list()
        return query

    def pr_approved(self, project, repo, pr):
        """
        Returns True if at least one reviewer approved the pull request, otherwise False.

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

    def open_pr_in_repo(self, project, repo, src_branch, dst_branch, title, desc, reviewers=None):
        """
        Opens a new pull request in a repository.
        """
        self.open_pr(project, repo, src_branch, project, repo, dst_branch, title, desc, reviewers)

    def open_pr(self, src_project, src_repo, src_branch, dst_project, dst_repo, dst_branch, title, desc, reviewers=None):
        """
        Opens a new pull request.
        """
        self.api.open_pull_request(src_project, src_repo, dst_project,
                                   dst_repo, src_branch, dst_branch, title, desc, reviewers)
