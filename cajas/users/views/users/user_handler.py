
from .create_user import CreateUser


class UsersHandler(object):
    """
    """

    @staticmethod
    def create_user(data):
        return CreateUser(data).call()
