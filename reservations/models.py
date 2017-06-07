from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Reservation(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    room_number = models.IntegerField(db_index=True)
    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        self.clean()
        return super(Reservation, self).save(*args, **kwargs)

    def clean(self):
        is_overlaps = (
            Reservation.objects.filter(
                room_number=self.room_number,
                start_date__lte=self.end_date,
                end_date__gte=self.start_date,
            ).exclude(
                id=self.id,
            ).exists()
        )
        if is_overlaps:
            raise ValidationError('Room is already booked for this dates')

    class Meta:
        index_together = (
            ('start_date', 'end_date'),
        )
