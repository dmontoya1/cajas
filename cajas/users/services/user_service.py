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
        daily_square = False
        email = ""
        try:
            user = User.objects.get(email=data['email'])
        except:
            if data['is_daily_square'] == "true":
                daily_square = True
            if data['email']:
                email = data['email']
                username = email
            else:
                username = data['document_id']
            user = User.objects.create(
                email=email,
                username=username,
                first_name=data['first_name'],
                last_name=data['last_name'],
                document_type=data['document_type'],
                document_id=data['document_id'],
                is_active=True,
                is_daily_square=daily_square
            )
            if "password1" in data:
                user.password = make_password(data['password1'])
                user.is_abstract = True
            else:
                user.is_abstract = False

            user.save()
        return user
