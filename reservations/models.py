from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class ReservationManager(models.Manager):
    def get_queryset(self):
        return super(
            ReservationManager, self
        ).get_queryset().filter(deleted=False)


class Reservation(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    room_number = models.IntegerField(db_index=True)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False, db_index=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    objects = ReservationManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        self.clean()
        return super(Reservation, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

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
