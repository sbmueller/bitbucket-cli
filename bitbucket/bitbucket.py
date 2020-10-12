#!/usr/bin/python3

import argparse
import logging

from server import Server
from config import Config


CONFIGFILE = os.path.join(os.path.expanduser("~"), ".config", "bitbucket-cli", "config.json")

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
    parser_pr.add_argument("action", choices=["approved", "open"])
    parser_pr.add_argument("project")
    parser_pr.add_argument("repository")
    parser_pr.add_argument("--prid", metavar="pr-id", required=False)
    parser_pr.add_argument("--src", required=False)
    parser_pr.add_argument("--dst", required=False)

    # parse arguments
    parsed = parser.parse_args()

    # TODO remove
    print(parsed)

    config = Config(CONFIGFILE)

    # if required arguments are not provided, try to read from config file
    if parsed.server is None:
        # try to get server from the yaml file
        logging.info("No server provided, trying to read from config file")
        parsed.server = config.get_config_value("server")
    if parsed.user is None:
        # try to get user from the yaml file
        logging.info("No user provided, trying to read from config file")
        parsed.user = config.get_config_value("user")
    if parsed.passwd is None:
        # try to get pass from the yaml file
        logging.info("No passwd provided, trying to read from config file")
        parsed.passwd = config.get_config_value("passwd")

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
        if parsed.action == "open":
            self.server.open_pr_in_repo(parsed.project, parsed.repository, parsed.src, parsed.dst, )
