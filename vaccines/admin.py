from django.contrib import admin
from .models import Vaccine, VaccineDose, SideEffectbyVaccine
# Register your models here.
from users.models import  UserProfile, UserVaccination, DependantProfile
from blog.models import Blog, Category

class DependantProfileAdmin(admin.ModelAdmin):
    list_display = ('user','Parent', 'Residence', 'Phone_Number', 'Date_of_birth', 'Gender', 'Weight', 'Height')
    search_fields =('user',)
    class Meta:
        model = DependantProfile

admin.site.register(DependantProfile, DependantProfileAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','National_ID', 'Residence', 'Phone_Number', 'Date_of_birth', 'Gender', 'Weight', 'Height')
    search_fields =('user',)
    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)


class UserVaccinationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'patient_vaccine', 'date_of_vaccine_reception', 'location_of_reception')

    class Meta:
        model = UserVaccination

admin.site.register(UserVaccination, UserVaccinationAdmin)

class VaccineAdmin(admin.ModelAdmin):
    list_display = ('vaccine_name', 'vaccine_ID_num', 'vaccine_Edition', 'about_Vaccine', 'child_Vaccine', 'last_update', 'vaccine_Dose_Count')

    class Meta:
        model = Vaccine


admin.site.register(Vaccine, VaccineAdmin)


class vaccinedoseAdmin(admin.ModelAdmin):
    list_display = ('vaccine', 'vaccine_dose', 'vaccine_dose_date_in_months', 'available',)
    search_fields = ('vaccine_dose',)
    list_editable = ('vaccine_dose', 'vaccine_dose_date_in_months','available',)

    class Meta:
        model = VaccineDose

admin.site.register(VaccineDose, vaccinedoseAdmin)


class SideEffectbyVaccineAdmin(admin.ModelAdmin):
    list_display = ('vaccine', 'sideEffectDesc')

    class Meta:
        model = SideEffectbyVaccine

admin.site.register(SideEffectbyVaccine, SideEffectbyVaccineAdmin)


class BlogAdmin(admin.ModelAdmin):
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)