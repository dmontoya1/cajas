from django.http import JsonResponse

from rest_framework.views import APIView

from cajas.office.models.officeItems import OfficeItems
from cajas.office.api.serializer.office_item_serializer import OfficeItemSerializer
from cajas.units.models.unitItems import UnitItems
from cajas.units.api.serializers.unit_items_serializer import UnitItemSerializer


class ReportActive(APIView):

    def get(self, request):
        data = dict()
        office_items = OfficeItems.objects.all()
        office_items_serializer = OfficeItemSerializer
        unit_items = UnitItems.objects.all()
        unit_items_serializer = UnitItemSerializer

        country = request.query_params.get('country', None)
        office_country = request.query_params.get('office_country', None)
        office = request.query_params.get('office', None)
        brand = request.query_params.get('brand', None)
        if brand:
            unit_items = unit_items.filter(brand__pk=brand)
            office_items = office_items.filter(brand__pk=brand)
        if office_country:
            office_items = office_items.filter(office=office_country)
            unit_items = unit_items.filter(unit__partner__office=office_country)
        elif office:
            office_items = office_items.filter(office__office=office)
            unit_items = unit_items.filter(unit__partner__office__office=office)
        elif country:
            office_items = office_items.filter(office__country=country)
            unit_items = unit_items.filter(unit__partner__office__country=country)

        data['office_items'] = office_items_serializer(office_items, many=True).data
        data['unit_items'] = unit_items_serializer(unit_items, many=True).data
        return JsonResponse(
            data,
            safe=False
        )
