
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cajas.inventory.models.brand import Brand
from cajas.boxes.models.box_partner import BoxPartner
from cajas.users.models.partner import Partner
from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.concepts.models.concepts import Concept, ConceptType
from cajas.concepts.services.stop_service import StopManager
from cajas.webclient.views.get_ip import get_ip
from ....services.partner_service import MovementPartnerManager
from cajas.units.models.units import Unit
from cajas.units.models.unitItems import UnitItems
from django.shortcuts import get_object_or_404


MovementPartnerManager = MovementPartnerManager()
email_manager = EmailManager()


class MovementPartnerCreate(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        partner = Partner.objects.get(pk=request.POST['partner_id'])
        box_partner = BoxPartner.objects.get(partner=partner)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']
        ip = get_ip(request)

        if concept.name == "Compra de Inventario Unidad":
            values = request.data["elemts"].split(",")
            if request.data["form[form]["+str(values[0])+"][name]"] != '':
                unit = Unit.objects.get(pk=request.data["unity"])
                for value in values:
                    UnitItems.objects.create(
                        unit=unit,
                        name=request.data["form[form]["+value+"][name]"],
                        brand=get_object_or_404(Brand, pk=request.data["form[form]["+value+"][brand]"]),
                        price=request.data["form[form]["+value+"][price]"]
                    )

        if concept.concept_type == ConceptType.SIMPLE:
            data = {
                'box': box_partner,
                'concept': concept,
                'date': date,
                'movement_type': movement_type,
                'value': value,
                'detail': detail,
                'responsible': request.user,
                'ip': ip,
                '_user': partner.user,
            }
            total_movements = MovementPartnerManager.get_user_value(data)
            stop_manager = StopManager(partner.user)
            stop = stop_manager.get_user_movements_top_value_by_concept(concept)
            informative_value = stop_manager.get_informative_user_top_value_movements_by_concept(concept)
            if informative_value != 0 and informative_value <= (total_movements['value__sum'] + int(data['value'])):
                email_manager.send_informative_top_notification(Site.objects.get_current().domain, partner.user, concept)
            if stop == 0 or(stop >= (total_movements['value__sum'] + int(data['value']))):
                movement = MovementPartnerManager.create_simple(data)
            else:
                return Response(
                    'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.',
                    status=status.HTTP_204_NO_CONTENT
                )

        elif concept.concept_type == ConceptType.DOUBLE:
            data = {
                'partner': partner,
                'box': partner.box,
                'concept': concept,
                'date': date,
                'movement_type': movement_type,
                'value': value,
                'detail': detail,
                'responsible': request.user,
                'ip': ip,
            }
            movement = MovementPartnerManager.create_double(data)
        elif concept.concept_type == ConceptType.SIMPLEDOUBLE:
            data = {
                'partner': partner,
                'concept': concept,
                'date': date,
                'movement_type': movement_type,
                'value': value,
                'detail': detail,
                'responsible': request.user,
                'ip': ip,
            }
            movement = MovementPartnerManager.create_simple_double(data)

        return Response(
            'Se ha añadido el movimiento exitosamente.',
            status=status.HTTP_201_CREATED
        )
