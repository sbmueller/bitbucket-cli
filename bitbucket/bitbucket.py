#!/usr/bin/python3

from atlassian import Bitbucket
import argparse
import logging
import json
import os


CONFIGFILE = os.path.join(os.path.expanduser("~"), ".config", "bitbucket-cli", "config.json")


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


def _get_config_value(key):
    """
    Reads the value for key from the config file.

    :param: key Key in JSON file
    """
    if not os.path.exists(CONFIGFILE):
        raise FileNotFoundError("Could not find config file at " + CONFIGFILE)
    with open(CONFIGFILE) as config:
        data = json.load(config)
    return data[key]


if __name__ == "__main__":
    # TODO set to warning
    logging.getLogger().setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description="BitBucket CLI")

    # general arguments
    parser.add_argument("-u", "--user", action="store", required=False,
                        help="Username for BitBucket. If not provided, will be read from config file.")
    parser.add_argument("-p", "--passwd", action="store", required=False,
                        help="Password or token for BitBucket. If not provided, will be read from config file.")
    parser.add_argument("-s", "--server", action="store", required=False,
                        help="URL for BitBucket server. If not provided, will be read from config file.")

    # create subparsers
    subparsers = parser.add_subparsers(dest="command")
    # project subparser
    parser_project = subparsers.add_parser("project")
    parser_project.add_argument("action", choices=["list"])
    # pull request subparser
    parser_pr = subparsers.add_parser("pr")
    parser_pr.add_argument("action", choices=["approved"])
    parser_pr.add_argument("project")
    parser_pr.add_argument("repository")
    parser_pr.add_argument("prid", metavar="pr-id")

    # parse arguments
    parsed = parser.parse_args()

    # TODO remove
    print(parsed)

    # if required arguments are not provided, try to read from config file
    if parsed.server is None:
        # try to get server from the yaml file
        logging.info("No server provided, trying to read from config file")
        parsed.server = _get_config_value("server")
    if parsed.user is None:
        # try to get user from the yaml file
        logging.info("No user provided, trying to read from config file")
        parsed.user = _get_config_value("user")
    if parsed.passwd is None:
        # try to get pass from the yaml file
        logging.info("No passwd provided, trying to read from config file")
        parsed.passwd = _get_config_value("passwd")

    # create a Server object
    server = Server(parsed.server, parsed.user, parsed.passwd)

    # decision tree for commands and actions
    if parsed.command == "project":
        if parsed.action == "list":
            print(server.project_list())
    if parsed.command == "pr":
        if parsed.action == "approved":
            print(server.pr_approved(parsed.project,
                                     parsed.repository, parsed.prid))
