
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

from cajas.loans.services.loan_service import LoanManager
from cajas.office.models.officeCountry import OfficeCountry

User = get_user_model()
loan_manager = LoanManager()


class LoanCreate(LoginRequiredMixin, View):
    """
    """

    def post(self, request, *args, **kwargs):
        value = request.POST['value']
        value_cop = request.POST['value_cop']
        interest = request.POST['interest']
        time = request.POST.get('time', None)
        exchange = request.POST['exchange']
        office = request.POST['office']
        office_obj = get_object_or_404(OfficeCountry, pk=office)
        loan_type = request.POST['loan_type']
        data = {
            'value': value,
            'value_cop': value_cop,
            'interest': interest,
            'time': time,
            'exchange': exchange,
            'office': office,
            'loan_type': loan_type,
            'date': request.POST['date'],
            'request': request
        }
        if loan_type == 'DIR':
            data['lender'] = request.POST['lender']
            loan = loan_manager.create_partner_loan(data)
        elif loan_type == 'EMP':
            box_from = request.POST['box_from']
            data['lender'] = request.POST['lender_employee']
            data['box_from'] = box_from
            if box_from == 'partner':
                data['provider'] = request.POST['partner_provider']
            loan = loan_manager.create_employee_loan(data)
        elif loan_type == 'TER':
            data['first_name'] = request.POST['third_first_name']
            data['last_name'] = request.POST['third_last_name']
            data['email'] = request.POST['third_email']
            data['document_type'] = request.POST['third_document_type']
            data['document_id'] = request.POST['third_document_number']
            data['description'] = request.POST['third_description']

            loan = loan_manager.create_third_loan(data)

        messages.add_message(request, messages.SUCCESS, 'Se ha registrado el préstamo exitosamente')
        return HttpResponseRedirect(reverse('webclient:loan_list', kwargs={'slug': office_obj.slug}))
