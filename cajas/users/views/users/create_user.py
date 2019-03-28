
from cajas.users.models.user import User


class CreateUser(object):

    def __init__(self, data):
        try:
            self._email = data['email']
            self._username = data['username']
            self._first_name = data['first_name']
            self._last_name = data['last_name']
            self._document_type = data['document_type']
            self._document_id = data['document_id']
        except:
            raise ValidationError('Todos los datos son obligatorios')

    def call(self):
        user = User.objects.create(
            email=self._email,
            username=self._username,
            first_name=self._first_name,
            last_name=self._last_name,
            document_type=self._document_type,
            document_id=self._document_id,
            is_active=True
        )
        user.save()
        return user
