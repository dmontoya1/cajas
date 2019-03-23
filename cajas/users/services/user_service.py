from django.contrib.auth.hashers import make_password

from ..models.user import User


class UserManager:
    """
    """

    PROPERTIES = ['email', 'first_name', 'last_name', 'document_type', 'document_id']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_user(self, data):
        self.__validate_data(data)
        if "password1" in data:
            try:
                user = User.objects.create(
                    email=data['email'],
                    username=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    document_type=data['document_type'],
                    document_id=data['document_id'],
                    password=make_password(data['password1']),
                    is_abstract=True,
                    is_active=True
                )
            except:
                raise Exception('Ha ocurrido un error al crear el usuario')
        else:
            try:
                user = User.objects.create(
                    email=data['email'],
                    username=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    document_type=data['document_type'],
                    document_id=data['document_id'],
                    is_abstract=False,
                    is_active=False
                )
            except:
                raise Exception('Ha ocurrido un error al crear el usuario')
        return user
