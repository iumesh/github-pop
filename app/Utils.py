import sys
import crayons
from settings import username, password


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def handle_connection_error():
        """
        Handles connection error
        """
        print(
            crayons.red(
                "Plz check you internet for connectivity. \n"
                "If internet is working then server my be temporarily down. \n"
                "Plz try after sometime."
            )
        )
        sys.exit()

    @staticmethod
    def handle_auth_error():
        """
        HAndles the auth error
        :return:
        """
        if username is None or password is None:
            print(
                crayons.red(
                    "You haven't declared the username and password in .env file"
                    "They should be declared like GITHUB_USERNAME=\"########\" \n"
                    "They should be declared like GITHUB_PASSWORD=\"########\" \n"
                )
            )
        else:
            print(
                crayons.red(
                    "Check if username and password is correct in .env file \n"
                )
            )