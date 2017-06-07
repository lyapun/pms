from rest_framework import serializers

from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'start_date', 'end_date', 'room_number', 'creator',
                  'created_at', 'updated_at', 'first_name', 'last_name')
