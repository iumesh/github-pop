from app.Organization import Organization
from app.Repo import Repo
import crayons
import argparse


def print_result(arguments):
    org_name = arguments.organization
    min_popular_repos = arguments.repos
    min_contributors = arguments.contributors

    print("Hang On! I am Fetching {} repos ...".format(crayons.green(arguments.organization)))

    # org name
    org = Organization(org_name)

    print("The organization {} has {} listed public repos.".format(
        org_name,
        crayons.green(org.public_repos)
    ))

    print(crayons.green('Fetching most popular repos ...'))

    # get repos
    repos = org.get_repos_by_popularity()

    max_repo_to_list = org.public_repos if min_popular_repos > org.public_repos else min_popular_repos

    i = 0
    while i < max_repo_to_list:

        print('{}. Repository Name: {} Forks: {}'.format(
            i + 1,
            crayons.green(repos[i]['name']),
            crayons.green(repos[i]['forks']))
        )

        repo_obj = Repo(
            name=repos[i]['name'],
            forks=repos[i]['forks'],
            full_name=repos[i]['full_name']
        )

        # get contributors
        contributors = repo_obj.get_contributors_by_contribution()

        max_contribs_to_list = len(contributors) if min_contributors > len(contributors) else min_contributors

        print(crayons.yellow("    Top contributors:"))

        j = 0
        while j < max_contribs_to_list:
            print('    -- {}.  User: {} Contributions: {}'.format(
                j + 1,
                crayons.green(contributors[j]['login']),
                crayons.green(contributors[j]['contributions']))
            )

            j = j + 1

        print("----------------")
        i = i + 1


def start_up():

    """Starting program execution .............."""

    # Create command line parser.
    parser = argparse.ArgumentParser(
        description="Exploring most popular github repos in an org and their top contributors"
    )

    # Adding command line arguments.
    parser.add_argument("organization", help="Github organization name", default=None)

    parser.add_argument("repos", help="Number of most popular repos to look into", type=int, default=None)

    parser.add_argument(
        "contributors",
        help="Number of top contributors to look for in each repo",
        type=int,
        default=None
    )

    # Parse command line arguments.
    arguments = parser.parse_args()

    print_result(arguments)


if __name__ == "__main__":
    start_up()
