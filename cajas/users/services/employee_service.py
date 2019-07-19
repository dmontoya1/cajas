
import logging

from ..models import Employee, DailySquareUnits

logger = logging.getLogger(__name__)


class EmployeeManager:
    """
    """

    PROPERTIES = ['user', 'office', 'charge', 'salary_type', 'salary']

    def __validate_data(self, data):
        for field in self.PROPERTIES:
            if field not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(field))

    def create_employee(self, data, aux):
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
            if employee.is_admin_charge():
                employee.office.add(aux['office'].office)
            else:
                employee.office_country.add(aux['office'])
        except Exception as e:
            logger.exception(str(e))
            raise Exception(e)
        return employee

    def delete_old_unit_from_daily_square_group(self, group):
        group.units.clear()
        group.delete()

    def add_new_units_to_group(self, group, units):
        for u in units:
            group.units.add(u)
        group.save()

    def update_daily_square_units_group(self, data):
        employee = Employee.objects.get(pk=data['employee'])
        old_group = DailySquareUnits.objects.get(employee=employee)
        self.delete_old_unit_from_daily_square_group(old_group)
        group = DailySquareUnits.objects.create(employee=employee)
        self.add_new_units_to_group(group, data.getlist("units[]"))
