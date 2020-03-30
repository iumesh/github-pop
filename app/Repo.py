import requests
from settings import username, password
import sys
from app.Utils import Utils


class Repo:

    def __init__(self, name=None, forks=None, full_name=None):
        """
        Constructor for repo
        :param name:  repo name
        :param forks:  repo forks
        :param full_name:  repo fullname
        """
        self.name = name
        self.forks = forks
        self.contributors = []
        self.full_name = full_name

    def get_contributors(self):
        """
        Get contributors
        :return:
        """
        if len(self.contributors) == 0:
            self.__fetch_contributors()

        return self.contributors

    # repos by count
    def get_contributors_by_contribution(self):
        """
        Sort contributors by contribution
        :return:
        """
        self.get_contributors()

        sorted(self.contributors, key=lambda x: x['contributions'], reverse=True)

        return self.contributors

    # fetch contributors
    def __fetch_contributors(self):
        """
        Fetch contributors via api
        :return:
        """

        try:
            resp = requests.get(
                "https://api.github.com/repos/{}/contributors?per_page=100".format(self.full_name),
                auth=(username, password)
            )

            if resp.status_code != 200:
                if resp.status_code == 401:
                    Utils.handle_auth_error()

                print(resp.status_code, resp.text)
                sys.exit()

            # add the contributor to contributors list
            contrib_list = resp.json()

            for contributor in contrib_list:
                self.contributors.append(contributor)

            link = resp.headers.get('link', None)

            if link is not None:
                # fetch last page number
                link_last = [l for l in link.split(',') if 'rel="last"' in l]
                last_page_no = int(link_last[0][link_last[0].find("&page=") + 6:link_last[0].find(">")])

                # fetch all the contributors
                for i in range(1, last_page_no + 1):
                    req = requests.get(
                        "https://api.github.com/repos/{}/contributors?per_page=100&page={}".format(self.full_name, i),
                        auth=(username, password)
                    )

                    if req.status_code != 200:
                        if resp.status_code == 401:
                            Utils.handle_auth_error()

                        print(resp.status_code, resp.text)
                        sys.exit()

                    contrib_list = req.json()

                    for contributor in contrib_list:
                        self.contributors.append(contributor)

        except requests.exceptions.ConnectionError:
            Utils.handle_connection_error()
