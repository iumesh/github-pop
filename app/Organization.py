import sys
import requests
import crayons
from settings import username, password
from app.Utils import Utils


class Organization:

    def __init__(self, name=None):
        """
        Constructor

        :param name: Name of organization
        """
        if name is None:
            print(crayons.red("Organization name not given"))
            sys.exit()

        self.id = None
        self.name = name
        self.public_repos = None
        self.org = None
        self.repos = []

        self.get_org()

    def get_org(self):
        """
        Gets the info of organization

        :return: dict
        """

        if self.org is None:
            self.org = self.__fetch_org()
            self.public_repos = self.org['public_repos']
            self.id = self.org['id']

        return self.org

    def get_repos_by_popularity(self):
        """
        Sorts the list of repos based on forks
        :return: list of dict
        """
        self.get_repos()

        sorted(self.repos, key=lambda x: x['forks'], reverse=True)

        return self.repos

    def get_repos(self):
        """
        Get the repos
        :return: list of dict
        """

        if len(self.repos) == 0 and self.org['public_repos'] != 0:
            self.__fetch_repos()

        return self.repos

    def __fetch_org(self):
        """
        Fetches the organization info from server

        :return:
        """
        try:
            resp = requests.get("https://api.github.com/orgs/{}".format(self.name), auth=(username, password))

            if resp.status_code != 200:
                if resp.status_code == 401:
                    Utils.handle_auth_error()

                print(resp.text)
                sys.exit()

            return resp.json()

        except requests.exceptions.ConnectionError:
            Utils.handle_connection_error()

    # fetch repo data
    def __fetch_repos(self):
        """
        Fetches the list of repos for org from server

        :return:
        """
        try:
            resp = requests.get(
                "https://api.github.com/orgs/{}/repos?per_page=100".format(self.name),
                auth=(username, password)
            )

            if resp.status_code != 200:
                if resp.status_code == 401:
                    Utils.handle_auth_error()

                print(crayons.red(resp.text))
                sys.exit()

            # add repo to repos list
            repos_list = resp.json()
            for repo in repos_list:
                self.repos.append(repo)

            link = resp.headers.get('link', None)

            # fetch last link page number
            if link is not None:
                # fetch last page number
                link_last = [l for l in link.split(',') if 'rel="last"' in l]
                last_page_no = int(link_last[0][link_last[0].find("&page=") + 6:link_last[0].find(">")])

                # fetch all the repos
                for i in range(1, last_page_no + 1):
                    req = requests.get(
                        "https://api.github.com/orgs/{}/repos?per_page=100&page={}".format(self.name, i),
                        auth=(username, password)
                    )

                    if req.status_code != 200:
                        if resp.status_code == 401:
                            Utils.handle_auth_error()

                        print(crayons.red(resp.text))
                        sys.exit()

                    repos_list = req.json()

                    for repo in repos_list:
                        self.repos.append(repo)

        except requests.exceptions.ConnectionError:
            Utils.handle_connection_error()
