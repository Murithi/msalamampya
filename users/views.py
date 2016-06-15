import datetime
import json
from django.views.generic import View
import forms
from django.core import serializers
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.messages.views import  SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.conf import settings
from django.contrib.auth.models import User
from vaccines.models import Vaccine, VaccineDose, SideEffectbyVaccine
from .models import UserProfile, UserVaccination, DependantProfile, Appointment, Doctor, Facility
from .forms import UserProfileForm, SignupForm, DependantProfileForm
from blog.models import Blog, Category

class UserPathMixin(object):

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs['username'])




@login_required
def home_page(request):
    return render(request, 'index.html', {})


def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        try:
            p = UserProfile.objects.get(user__username=request.POST['username'])
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect('userprofile')

        if p.National_ID is not None:
            request.session['user_sysID'] = p.National_ID
            return redirect('/home')
        else:
            return HttpResponseRedirect('userprofile')

    else:
        return HttpResponseRedirect('invalid_login.html')


def invalid_login(request):
    return render_to_response('invalid_login.html')


class SignUp(FormView):
    form_class = SignupForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def form_valid(self, form):
        form.instance.firstname = form.cleaned_data.get('firstname')
        form.instance.lastname = form.cleaned_data.get('lastname')
        form.instance.username = form.cleaned_data.get('username')
        form.instance.email = form.cleaned_data.get('email')
        form.instance.password1 = form.cleaned_data.get('password1')
        form.save()
        return HttpResponseRedirect(reverse('signup_success'))

def signup_success(request):
    return render_to_response('signup_success.html')

class addMemberProfiledetails(FormView):
    form_class = DependantProfileForm
    template_name='addmemberprofile.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form':form}, context_instance=RequestContext(request))

    def form_valid(self, form):
        userid = User.objects.get(id=self.request.session['new_user_ID'])
        form.instance.profilepic = form.cleaned_data.get('profilepic')
        form.instance.Date_of_birth = form.cleaned_data.get('Date_of_birth')
        form.instance.Height = form.cleaned_data.get('Height')
        form.instance. Weight = form.cleaned_data.get('Weight')
        form.instance.Gender = form.cleaned_data.get('Gender')
        form.instance.Residence = form.cleaned_data.get('Residence')
        form.instance.Phone_Number = form.cleaned_data.get('Phone_Number')
        form.instance.Parent = UserProfile.objects.get(user=self.request.user)
        form.instance.user = userid
        form.save()
        return redirect('/dashboard')


class AddMember(FormView):
    form_class = SignupForm
    template_name = 'addmember.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def form_valid(self, form):
        form.instance.firstname = form.cleaned_data.get('firstname')
        form.instance.lastname = form.cleaned_data.get('lastname')
        form.instance.username = form.cleaned_data.get('username')
        form.instance.email = form.cleaned_data.get('email')
        form.instance.password1 = form.cleaned_data.get('password1')
        form.save()
        newuser = form.save()
        self.request.session['new_user_ID']=newuser.id
        return HttpResponseRedirect(reverse('profiledetails-add'))

@login_required
def update_profile(request):
    userProfile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm()
    return render_to_response('update_profile.html', {'form': form}, RequestContext(request))


class UserProfileCreate(CreateView):
    form_class = UserProfileForm


class UserProfileUpdate(UpdateView):
    model = UserProfile
    form_class = UserProfileForm


class UserProfileDelete(DeleteView):
    model = UserProfile
    success_url = reverse_lazy('dashboard')


class your_profile(UpdateView):
    form_class = UserProfileForm
    template_name='update_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form':form}, context_instance=RequestContext(request))

    def form_valid(self, form):
        userProfile = UserProfile.objects.get(user=self.request.user)
        form.instance.profilepic = form.cleaned_data.get('profilepic')
        form.instance.Date_of_birth = form.cleaned_data.get('Date_of_birth')
        form.instance.Height = form.cleaned_data.get('Height')
        form.instance. Weight = form.cleaned_data.get('Weight')
        form.instance.Gender = form.cleaned_data.get('Gender')
        form.instance.Residence = form.cleaned_data.get('Residence')
        form.instance.Phone_Number = form.cleaned_data.get('Phone_Number')
        form.instance.National_ID = form.cleaned_data.get('National_ID')
        form.instance.Dependant = form.cleaned_data.get('Dependant')
        form.instance.user = self.request.user
        form.save()
        return redirect('/dashboard')

def user_profile(request):
    return render(request, 'user.html')

def view_profile(request, user):

    parent = UserProfile.objects.get(Q(user=request.user) & Q(Dependant=False))
    dependants = UserProfile.objects.filter(Q(user=request.user) & Q(Dependant=True))

    return render(request, 'dashboard.html', {'alldependants': dependants, 'parent': parent})


def dashboard(request):
    parent = UserProfile.objects.filter(user=request.user)
    dependants = DependantProfile.objects.filter(Parent=parent)
    return render(request, 'dashboard.html', {'alldependants':dependants, 'parents': parent})


def patient_profile(request):
    print request.GET.get('pk')
    # thisuser= User.objects.get(id=request.GET.get('pk'))
    thisuser=request.GET.get('pk')
    months = lambda a, b: abs((a.year - b.year) * 12 + a.month - b.month)

    if UserProfile.objects.filter(user=thisuser).exists():
        birthday = UserProfile.objects.get(user=thisuser)
        age = months(datetime.date.today(), birthday.Date_of_birth)
        if age > 12:
            age = age / 12
        patient_details = UserProfile.objects.get(user=thisuser)
    else:
        patient_details = DependantProfile.objects.get(user=thisuser)
        birthday = DependantProfile.objects.get(user=thisuser)
        age = months(datetime.date.today(), birthday.Date_of_birth)
        if age > 12:
            age = age / 12
    Received_Vaccines = VaccineDose.objects.filter(uservaccination__patient=thisuser).order_by(
        "vaccine_dose_date_in_months")
    All_Vaccines = VaccineDose.objects.all().order_by("vaccine_dose_date_in_months")
    Remaining_Vaccines = [item for item in All_Vaccines if item not in Received_Vaccines]

    return render(request, 'patientdetails.html', {'patientdetails': patient_details, 'dependantage': age,
                                                     'vaccinesrecieved': Received_Vaccines,
                                                     'vaccinesrequired': Remaining_Vaccines})


def patientvaccinedetails(request):
    vacid = request.GET['id']

    thisvaccine = VaccineDose.objects.get(id=vacid).vaccine


    # Get count of doses
    vaccdosescount = VaccineDose.objects.filter(vaccine=thisvaccine).count()

    count = UserVaccination.objects.filter(patient=request.user).filter(
        patient_vaccine=thisvaccine).count()
    #PERCENTAGE DOSES RECIEVED
    percentagevaccinated = 0
    if count:
        if vaccdosescount:
            percentagevaccinated = int(count / float(vaccdosescount) * 100)

    #ALL DOSES REQUIRED
    vaccinedoses = VaccineDose.objects.filter(vaccine=thisvaccine).order_by("vaccine_dose")

    #DOSES RECIEVED SO FAR
    vaccinedosesrecieved = UserVaccination.objects.filter(patient=request.user).filter(
        patient_vaccine=thisvaccine)
    vaccinedosesrecieved_list = [vaccine.vaccine_dose for vaccine in vaccinedosesrecieved]

    if UserProfile.objects.filter(user=1).filter(Dependant=True).count()>0:
        birthdate = UserProfile.objects.get(Q(user=request.user) & Q(Dependant=True)).Date_of_birth

        vaccinationdate = [birthdate + datetime.timedelta(days=(item.vaccine_dose_date_in_months * 3)) for item in
                       vaccinedoses]
        for item in vaccinedoses:
            item.vaccine_dose_date_in_months = birthdate + datetime.timedelta(days=(item.vaccine_dose_date_in_months * 3))

    pending = [item for item in vaccinedoses if item not in vaccinedosesrecieved_list]
    received = [item for item in vaccinedoses if item in vaccinedosesrecieved_list]
    sideeffects = SideEffectbyVaccine.objects.filter(vaccine=thisvaccine)


    return render(request, 'patientvaccinelist.html', {'percentagedose': percentagevaccinated,
                                                       'vaccinesrecieved': received, 'vaccinesrequired': pending,
                                                       'mainvaccine': thisvaccine, 'sideeffects': sideeffects,
                                                       'alldoses': vaccinedoses})


def vaccinetype(request):
    return render(request, 'vaccinetype.html')


def childvaccines(request):
    vaccines = Vaccine.objects.all()
    return render(request, 'childvaccines.html', {'allvaccines': vaccines, 'thisuser':request.user})


def vaccinelist(request):
    vacid = request.GET['id']
    thisuser= User.objects.get(id =request.GET.get('pk'))

    thisvaccine = Vaccine.objects.get(id=vacid)


    # Get count of doses
    vaccdosescount = VaccineDose.objects.filter(vaccine=thisvaccine).count()

    count = UserVaccination.objects.filter(patient=thisuser).filter(
        patient_vaccine=thisvaccine).count()
    #PERCENTAGE DOSES RECIEVED
    percentagevaccinated = 0
    if count:
        if vaccdosescount:
            percentagevaccinated = int(count / float(vaccdosescount) * 100)

    #ALL DOSES REQUIRED


    vaccinedoses = VaccineDose.objects.filter(vaccine=thisvaccine).order_by("vaccine_dose")

    #DOSES RECIEVED SO FAR

    vaccinedosesrecieved = UserVaccination.objects.filter(patient=thisuser).filter( patient_vaccine=thisvaccine)
    vaccinedosesrecieved_list = [vaccine.vaccine_dose for vaccine in vaccinedosesrecieved]

    if UserProfile.objects.filter(user=thisuser).filter(Dependant=True).count()>0:
        birthdate = UserProfile.objects.get(Q(user=thisuser) & Q(Dependant=True)).Date_of_birth

        vaccinationdate = [birthdate + datetime.timedelta(days=(item.vaccine_dose_date_in_months * 3)) for item in
                       vaccinedoses]
        for item in vaccinedoses:
            item.vaccine_dose_date_in_months = birthdate + datetime.timedelta(days=(item.vaccine_dose_date_in_months * 3))


    pending = [item for item in vaccinedoses if item not in vaccinedosesrecieved_list]
    received = [item for item in vaccinedoses if item in vaccinedosesrecieved_list]
    sideeffects = SideEffectbyVaccine.objects.filter(vaccine=thisvaccine)

    print DependantProfile.objects.filter(user=thisuser).count()
    if DependantProfile.objects.filter(user=thisuser).count() != 0:
        parent = DependantProfile.objects.get(user=thisuser).Parent

    else:
        parent = UserProfile.objects.get(Q(user=thisuser) & Q(Dependant=False))

    dependants = DependantProfile.objects.filter(Parent=parent)

    return render(request, 'patientvaccinelistbyvaccine.html', {'percentagedose': percentagevaccinated,
                                                                'vaccinesrecieved': received,
                                                                'vaccinesrequired': pending,
                                                                'mainvaccine': thisvaccine, 'sideeffects': sideeffects,
                                                                'alldoses': vaccinedoses, 'alldependants': dependants,
                                                                'parent': parent, 'thisuser':thisuser})


def emaillist(request):
    return render(request, 'mail.html')

class MessagesView(UserPathMixin, SingleObjectMixin, ListView):
    paginate_by = 2
    template_name = "mail.html"

    def get_queryset(self):
        self.object = self.get_object()
        if self.object == self.request.user:
            raise Http404
        result = Message.objects.concrete_user(self.request.user, self.object).order_by('-sent_at')
        answ = result.filter(recipient=self.request.user).update(read_at=now())
        return result

    def get_context_data(self, **kwargs):
        context = super(MessagesView, self).get_context_data(**kwargs)
        context['view_tab'] = 'user_messages'
        return context


class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""

    model = Appointment
    fields = ['name', 'phone_number', 'doctor', 'time', 'time_zone']
    success_message = 'Appointment successfully created.'


class AppointmentListView(ListView):
    """Shows users a list of appointments"""

    model = Appointment


class AppointmentDetailView(DetailView):
    """Shows users a single appointment"""

    model = Appointment

class AppointmentUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    success_message = 'Appointment successfully updated.'


class AppointmentDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Appointment
    success_url = reverse_lazy('list_appointments')



#### BLOG APP

def index(request):
       return render_to_response('blog.html', {
        'categories': Category.objects.all(),
        'posts':Blog.objects.order_by('-timestamp')[0],
        'otherposts': Blog.objects.order_by("-timestamp")[1:4],
        'recentnews': Blog.objects.order_by("-timestamp")[4:5]
    })

def view_post(request, slug):
    return render_to_response('view_post.html', {
        'post': get_object_or_404(Blog, slug=slug)
    })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('blogcategory.html', {
        'category': category,
        'posts': Blog.objects.filter(category=category)[:5]
    })
def default(o):
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()

class UsersView(View):
    def get(self, request, *args, **kwargs):
        data_type = request.GET.get('type')


        username = self.kwargs['pk']

        if username is not None:

            Usaggregate = User.objects.none()
            Usaggregate = list(Usaggregate) + list(User.objects.filter(id=username).values('username','first_name', 'last_name', 'id'))
            ID = DependantProfile.objects.filter(Parent=username)
            for item in ID:
                Usaggregate = list(Usaggregate) + list(User.objects.filter(id=item.user.id).values('username','first_name', 'last_name', 'id'))

            user_data = Usaggregate

            Vaccine_Dose_Aggregate = VaccineDose.objects.none()
            Vaccine_Dose_Aggregate = list(Vaccine_Dose_Aggregate) + list(VaccineDose.objects.all().values('vaccine', 'vaccine_dose',
                                                                   'vaccine_dose_date_in_months', 'id'))
            vaccine_dose_data =Vaccine_Dose_Aggregate


            # VACCINES DATA

            allvaccines=[]
            parentvaccs=[]
            savedvaccs = Vaccine.objects.all()
            key=0
            for vacc in savedvaccs:
                Gcount=UserVaccination.objects.filter(patient=username, patient_vaccine=vacc.id).count()

                if Gcount > 0:
                    G = UserVaccination.objects.filter(patient=username, patient_vaccine=vacc.id)

                    dosecount =UserVaccination.objects.filter(patient=username, patient_vaccine=vacc.id).count()
                    perc = float(dosecount)/float(vacc.vaccine_Dose_Count)*100
                    vaccusername = G[0].patient.username
                    key=(key+1)
                    allvaccines.append({"vaccinekey":key, "name":vaccusername, "vaccine_ID_num": vacc.id, "vaccine_name":vacc.vaccine_name, "percentage": perc})
                else:
                    thisUser = User.objects.get(id=username)
                    key = (key + 1)
                    allvaccines.append({"vaccinekey": key,
                        "name": thisUser.username, "vaccine_ID_num": vacc.id, "vaccine_name": vacc.vaccine_name,
                         "percentage": 0})

            kids = DependantProfile.objects.filter(Parent=username)
            for kid in kids:
                for vacc in savedvaccs:
                    G = UserVaccination.objects.filter(patient=kid.user, patient_vaccine=vacc.id)
                    if Gcount > 0:
                        dosecount = UserVaccination.objects.filter(patient=kid.user, patient_vaccine=vacc.id).count()
                        perc = float(dosecount) / float(vacc.vaccine_Dose_Count) * 100
                        vaccusername=kid.user.username
                        key = (key + 1)
                        allvaccines.append({"vaccinekey": key,"name": vaccusername, "vaccine_ID_num": vacc.id, "vaccine_name": vacc.vaccine_name,
                             "percentage": perc})
                    else:
                        thisUser = User.objects.get(id=username)
                        key = (key + 1)
                        allvaccines.append({"vaccinekey": key,"name": kid.user.username, "vaccine_ID_num": vacc.id, "vaccine_name": vacc.vaccine_name,
                             "percentage": 0})


            parentrecs = UserVaccination.objects.filter(patient=username)
            childrenID = DependantProfile.objects.filter(Parent=username)
            doses = VaccineDose.objects.all()

            family_doses = {}
            recievedparentdose=[]
            testchild=[]

            parent_doses = []
            for parent in parentrecs:
                recievedparentdose= [dose for dose in parent.vaccine_dose.all()]



            for dose in doses:


                    if dose in recievedparentdose:
                        parent_doses.append({"name": parent.patient.username, "vaccine_ID":dose.vaccine.id, "vaccine_name": dose.vaccine.vaccine_name,"vaccine_dose_id":dose.id, "vaccine_dose": dose.vaccine_dose,
                                        "vaccination_date": dose.vaccine_dose_date_in_months, "received": 1})
                    else:
                        parent_doses.append({"name": parent.patient.username, "vaccine_ID":dose.vaccine.id, "vaccine_name": dose.vaccine.vaccine_name,"vaccine_dose_id":dose.id, "vaccine_dose": dose.vaccine_dose,
                                        "vaccination_date": dose.vaccine_dose_date_in_months, "received": 0})



            # test.append({"name": parentrecs[0].patient.first_name})
            # family_doses[repr(test)] = parent_doses

            child_doses = []
            # received_doses=[]
            for child in childrenID:
                childrenrecs = UserVaccination.objects.filter(patient=child.user)
                for childrec in childrenrecs:
                    # received_doses = childrec.vaccine_dose.all()
                    received_doses = [dose for dose in childrec.vaccine_dose.all()]
            # for childrec in childrenrecs:
            for dose in doses:
                if dose in received_doses:
                    child_doses.append({"name": child.user.username, "vaccine_ID":dose.vaccine.id, "vaccine_name": dose.vaccine.vaccine_name,"vaccine_dose_id":dose.id, "vaccine_dose": dose.vaccine_dose,
                                        "vaccination_date": dose.vaccine_dose_date_in_months, "received": 1})


                else:
                    child_doses.append({ "name": child.user.username, "vaccine_ID":dose.vaccine.id, "vaccine_name": dose.vaccine.vaccine_name,"vaccine_dose_id":dose.id, "vaccine_dose": dose.vaccine_dose,
                                        "vaccination_date": dose.vaccine_dose_date_in_months, "received": 0})






            testchild.append({})

            patient_data = child_doses + parent_doses
            print len(patient_data)



            Doctor_Aggregate = Doctor.objects.none()
            Doctor_Aggregate = list(Doctor_Aggregate) + list(
                Doctor.objects.all().values('user__username', 'facility__facility_name'))
            doctor_data = Doctor_Aggregate


            qs = Appointment.objects.filter(owner__id=username)
            qs = qs.extra(
                select={'appointment_date': "to_char(time, 'YYYY-MM-DD HH24:MI:SS')"})
            # Appointment_Aggregate = Appointment.objects.none()
            # Appointment_Aggregate = list(Appointment_Aggregate) + list(
            #     qs.values('id', 'name', 'appointment_date', 'doctor__first_name', 'owner')
            # )
            Appointmentdetails=[]
            Appts = Appointment.objects.filter(owner__id = username)
            for apptmt in qs:
                K=apptmt.doctor.all()
                G=K[0].user
                M=apptmt.facility.all()

                Appointmentdetails.append({"owner": username, "doctor": G.first_name, "id": apptmt.id,  "appointment_date": apptmt.appointment_date,
                                    "name": apptmt.name, "status": 0, "location": M[0].facility_name})
            appointment_data= Appointmentdetails



        data =  {'users': user_data, 'vaccines':allvaccines, 'vaccine_doses':vaccine_dose_data,
                 'patient_vaccines':patient_data, 'doctors': doctor_data,'appointments': appointment_data}

        return HttpResponse(json.dumps(data), content_type='application/json')