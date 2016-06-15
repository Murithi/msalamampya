from django.utils.encoding import smart_unicode
from django.db import models
from django.db import connection


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

class VaccineDoseManager(models.Manager):
    def get_queryset(self, params=()):
        """Execute a raw query and return a QuerySet.  The first column in the
        result set must be the id field for the model.
        :type raw_query: str | unicode
        :type params: tuple[T] | dict[str | unicode, T]
        :rtype: django.db.models.query.QuerySet
        """

        cursor = connection.cursor()
        raw_query ="""select vaccinedose.id as vaccinedoseID, vaccine_dose, vaccine_id, to_char(date_of_vaccine_reception, 'YYYY-MM-DD HH24:MI:SS'),
   coalesce(users_uservaccination.patient_id, 0) as status from vaccines_vaccinedose
   left join users_uservaccination on users_uservaccination.vaccine_dose_id = vaccines_vaccinedose.id and patient_id IN (""" + params + """) order by vaccine_id, vaccine_dose"""



        try:
            cursor.execute(raw_query)
            row=cursor.fetchall()
            return list(row)
        finally:
            cursor.close()

class VaccineDose(models.Model):
    vaccine = models.ForeignKey(Vaccine)
    vaccine_dose = models.CharField(max_length=150)
    vaccine_dose_date_in_months = models.IntegerField()
    available = models.BooleanField()
    # The default manager.
    # mobjects = VaccineDoseManager() # The specific manager.
    # objects = models.Manager

    def __unicode__(self):
        return smart_unicode(self.vaccine_dose)




class SideEffectbyVaccine(models.Model):
    vaccine = models.ForeignKey(Vaccine)
    sideEffectDesc = models.CharField(max_length=80)

    def __unicode__(self):
        return smart_unicode(self.sideEffectDesc)
