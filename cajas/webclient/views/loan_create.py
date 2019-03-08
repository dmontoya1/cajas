
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

from cajas.users.models.employee import Employee
from loans.services.loan_service import loan_manager
from office.models.office import Office

User = get_user_model()


class LoanCreate(LoginRequiredMixin, View):
    """
    """

    def post(self, request, *args, **kwargs):
        value = request.POST['value']
        value_cop = request.POST['value_cop']
        interest = request.POST['interest']
        time = request.POST['time']
        exchange = request.POST['exchange']
        office = request.POST['office']
        office_obj = get_object_or_404(Office, pk=office)
        loan_type = request.POST['loan_type']
        data = {
            'value': value,
            'value_cop': value_cop,
            'interest': interest,
            'time': time,
            'exchange': exchange,
            'office': office,
            'loan_type': loan_type,
            'request': request
        }
        if loan_type == 'DIR':
            data['lender'] = request.POST['lender']
            loan = loan_manager.create_partner_loan(data)
        elif loan_type == 'EMP':
            lender = request.POST['lender_employee']
            lender = lender.user
            box_from = request.POST['box_from']
            data['lender'] = lender
            data['box_from'] = box_from
            if box_from == 'partner':
                data['provider'] = request.POST['provider']
            loan = loan_manager.create_employee_loan(data)
        elif loan_type == 'TER':
            loan = loan_manager.create_third_loan(data)

        messages.add_message(request, messages.SUCCESS, 'Se ha registrado el préstamo exitosamente')
        return HttpResponseRedirect(reverse('webclient:loan_list', kwargs={'slug': office_obj.slug}))
