# from appointments.settings import celery_app
import pytz
import arrow
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode
from django.utils.encoding import python_2_unicode_compatible
from timezone_field import TimeZoneField
from vaccines.models import Vaccine, VaccineDose
from django.core.urlresolvers import reverse_lazy, reverse

def upload_location(instance, filename):
    return "%s/%s" %(instance.user, filename)

class UserProfile(models.Model):
    GENDER_CHOICES = (('m', 'Male'), ('f', 'Female'))
    user = models.OneToOneField(User, primary_key=True)
    profilepic = models.ImageField(upload_to=upload_location,
                                   null=True,
                                   blank=True,
                                   width_field="width_field",
                                   height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    Date_of_birth = models.DateField(default=timezone.now)
    Height = models.CharField(max_length=3)
    Weight = models.CharField(max_length=3)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Residence = models.CharField(max_length=200)
    Phone_Number = models.CharField(max_length=10)
    Updated_at=models.DateTimeField(auto_now_add=False, auto_now=True)
    National_ID = models.CharField(max_length=8, unique=False, blank=True)
    Dependant = models.BooleanField(default=False)

    def get_absolute_url(self):
       return reverse('profile', kwargs={'pk': self.pk})

    def __unicode__(self):
        return smart_unicode(self.user.username)


    from django.db.models.signals import post_save
    from django.dispatch import  receiver
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            profile, new = UserProfile.objects.get_or_create(user=instance)


class DependantProfile(models.Model):
    GENDER_CHOICES = (('m', 'Male'), ('f', 'Female'))
    user = models.OneToOneField(User, primary_key=True)
    profilepic = models.ImageField(upload_to=upload_location,
                                   null=True,
                                   blank=True,
                                   width_field="width_field",
                                   height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    Date_of_birth = models.DateField(default=timezone.now)
    Height = models.CharField(max_length=3)
    Weight = models.CharField(max_length=3)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Residence = models.CharField(max_length=200)
    Phone_Number = models.CharField(max_length=10)
    Updated_at=models.DateTimeField(auto_now_add=False, auto_now=True)
    Parent = models.ForeignKey(UserProfile)
    Dependant = models.BooleanField(default=True)

    def get_absolute_url(self):
       return reverse('profile', kwargs={'pk': self.pk})

    def __unicode__(self):
        return smart_unicode(self.user.username)


    from django.db.models.signals import post_save
    from django.dispatch import  receiver
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            profile, new = UserProfile.objects.get_or_create(user=instance)

class UserVaccination(models.Model):
    patient = models.ForeignKey(User)
    creation_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    patient_vaccine = models.ForeignKey(Vaccine)
    vaccine_dose = models.ForeignKey(VaccineDose)
    date_of_vaccine_reception = models.DateTimeField()
    location_of_reception = models.CharField(max_length=150, blank=True)
    Timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return smart_unicode(self.patient)


class AppointmentOld(models.Model):
    firstchoicedate=models.DateTimeField()
    secondchoicedate=models.DateTimeField()
    purposeofvisit=models.CharField(max_length=600)
    patient = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return smart_unicode(self.patient.user.first_name, self.patient.user.last_name)

# @python_2_unicode_compatible
class Appointment(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='Africa/Nairobi')

    # Additional fields not visible to users
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Appointment #{0} - {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('view_appointment', args=[str(self.id)])

    def clean(self):
        """Checks that appointments are not scheduled in the past"""

        appointment_time = arrow.get(self.time, self.time_zone.zone)

        if appointment_time < arrow.utcnow():
            raise ValidationError('You cannot schedule an appointment for the past. Please check your time and time_zone')

    def schedule_reminder(self):
        """Schedules a Celery task to send a reminder about this appointment"""

        # Calculate the correct time to send this reminder
        appointment_time = arrow.get(self.time, self.time_zone.zone)
        reminder_time = appointment_time.replace(minutes=-settings.REMINDER_TIME)

        # Schedule the Celery task
        from .tasks import send_sms_reminder
        result = send_sms_reminder.apply_async((self.pk,), eta=reminder_time)

        return result.id
    def save(self, *args, **kwargs):
        """Custom save method which also schedules a reminder"""

        # Check if we have scheduled a reminder for this appointment before
        if self.task_id:
            # Revoke that task in case its time has changed
            celery_app.control.revoke(self.task_id)

        # Save our appointment, which populates self.pk,
        # which is used in schedule_reminder
        super(Appointment, self).save(*args, **kwargs)

        # Schedule a new reminder task for this appointment
        self.task_id = self.schedule_reminder()

        # Save our appointment again, with the new task_id
        super(Appointment, self).save(*args, **kwargs)
class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    facility_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

class DailySchedule(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='day_schedule')
    date = models.DateField()
    schedule = models.CharField(max_length=96)
