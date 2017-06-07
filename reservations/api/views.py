from rest_framework import viewsets

from reservations.models import Reservation

from .serializers import ReservationSerializer
from .permissions import ReservationPermissions


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (ReservationPermissions, )

    def get_queryset(self):
        queryset = Reservation.objects.all()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date is not None:
            queryset = queryset.filter(end_date__gte=start_date)
        if end_date is not None:
            queryset = queryset.filter(start_date__lte=end_date)
        return queryset
