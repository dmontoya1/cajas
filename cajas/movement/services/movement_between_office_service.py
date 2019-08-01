

from cajas.movement.models.movement_between_office_request import MovementBetweenOfficeRequest


class MovementBetweenOfficesManager(object):

    def create_between_offices_movement_request(self, data, movement_pk, origin_type):
        if data['movement_type'] == 'OUT':
            contrapart = 'IN'
        else:
            contrapart = 'OUT'
        MovementBetweenOfficeRequest.objects.create(
            box_office=data['destine_office'].box,
            origin_office=data['office'].box,
            from_box_type=origin_type,
            origin_movement_pk=movement_pk,
            observation=data['detail'],
            detail=data['detail'],
            concept=data['concept'],
            movement_type=contrapart,
            date=data['date'],
            value=data['value'],
            responsible=data['responsible'],
            ip=data['ip'],
        )
