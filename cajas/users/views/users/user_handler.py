
from .create_user import CreateUser


class UsersHandler(object):
    """
    """

    @classmethod
    def create_user(cls, data):
        return CreateUser(data).call()
