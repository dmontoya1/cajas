from django.contrib.auth.hashers import make_password

from ..models.user import User


class UserManager:
    """
    """

    PROPERTIES = ['email', 'first_name', 'last_name', 'document_type', 'document_id', 'is_daily_square']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_user(self, data):
        self.__validate_data(data)
        try:
            user = User.objects.get(username=data['email'])
        except:
            user = User.objects.create(
                email=data['email'],
                username=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                document_type=data['document_type'],
                document_id=data['document_id'],
                is_active=True,
                is_daily_square=data['is_daily_square']
            )
            if "password1" in data:
                user.password = make_password(data['password1'])
                user.is_abstract = True
            else:
                user.is_abstract = False
            if data["is_daily_square"] == "true":
                user.is_daily_square = True

            user.save()
        return user
