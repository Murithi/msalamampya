from django.utils.encoding import smart_unicode
from django.db import models


# Create your models here.
class Vaccine(models.Model):
    vaccine_name=models.CharField(max_length=200)
    vaccine_ID_num=models.CharField(max_length=150)
    vaccine_Edition=models.CharField(max_length=150)
    about_Vaccine=models.CharField(max_length=500)
    child_Vaccine=models.BooleanField(default=True)
    last_update  =models.DateField(auto_now_add=False, auto_now=True)
    image = models.ImageField(upload_to="images/", null=True)
    vaccine_Dose_Count = models.CharField(max_length=50)
    timestamp= models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return smart_unicode(self.vaccine_name)


class VaccineDose(models.Model):
    vaccine = models.ForeignKey(Vaccine)
    vaccine_dose = models.CharField(max_length=150)
    vaccine_dose_date_in_months = models.IntegerField()
    available = models.BooleanField()

    def __unicode__(self):
        return smart_unicode(self.vaccine_dose)


class SideEffectbyVaccine(models.Model):
    vaccine = models.ForeignKey(Vaccine)
    sideEffectDesc = models.CharField(max_length=80)

    def __unicode__(self):
        return smart_unicode(self.sideEffectDesc)
