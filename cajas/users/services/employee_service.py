
from ..models.employee import Employee


class EmployeeManager:
    """
    """

    PROPERTIES = ['user', 'office', 'charge', 'salary_type', 'salary']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_employee(self, data):
        self.__validate_data(data)
        try:
            employee = Employee.objects.create(
                user=data['user'],
                office=data['office'],
                charge=data['charge'],
                salary_type=data['salary_type'],
                salary=data['salary'],
                cv=data['cv'],
                passport=data['passport'],
            )
        except:
            raise Exception('Ha ocurrido un error al crear el usuario')
        return employee


employee_manager = EmployeeManager()
