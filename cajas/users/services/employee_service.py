
import logging

from ..models.employee import Employee

logger = logging.getLogger(__name__)


class EmployeeManager:
    """
    """

    PROPERTIES = ['user', 'office', 'charge', 'salary_type', 'salary']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_employee(self, data, aux):
        self.__validate_data(data)
        try:
            employee = Employee.objects.create(
                user=aux['user'],
                charge=aux['charge'],
                salary_type=data['salary_type'],
                salary=float(data['salary']),
                cv=data['cv'],
                passport=data['passport'],
            )
            employee.save()
            if data['user'].related_employee.get().is_admin_charge():
                employee.office.add(aux['office'].office)
            else:
                employee.office_country.add(aux['office'])
        except Exception as e:
            logger.exception(str(e))
            raise Exception(e)
        return employee


employee_manager = EmployeeManager()
