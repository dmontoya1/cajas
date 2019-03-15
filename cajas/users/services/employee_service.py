
from ..models.employee import Employee


class EmployeeManager:
    """
    """

    PROPERTIES = ['user', 'office', 'charge', 'salary_type', 'salary', 'passport', 'cv']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_user(self, data):
        self.__validate_data(data)
        try:
            employee = Employee.objects.create(
                user=data['user'],
                office=data['office'],
                charge=data['charge'],
                salary_type=data['salary_type'],
                salary=data['salary'],
                passport=data['passport'],
                cv=data['cv']
            )
        except:
            raise Exception('Ha ocurrido un error al crear el usuario')
        return employee


employee_manager = EmployeeManager()
