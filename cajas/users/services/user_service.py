
from ..models.user import User


class UserManager:
    """
    """

    PROPERTIES = ['email', 'username', 'first_name', 'last_name', 'document_type', 'document_id']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_user(self, data):
        self.__validate_data(data)
        try:
            user = User.objects.create(
                email=data['email'],
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                document_type=data['document_type'],
                document_id=data['document_id']
            )
        except:
            raise Exception('Ha ocurrido un error al crear el usuario')
        return user
