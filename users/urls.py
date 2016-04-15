from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from users import views
urlpatterns = [
    url(r'^$', 'users.views.login', name='login'),
    url(r'^login', 'users.views.login', name='login'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^signup_success/$', 'users.views.signup_success', name='signup_success'),
    url(r'^home', 'users.views.home_page', name='home_page'),
    url(r'^auth', 'users.views.auth_view', name='auth'),
    url(r'^invalid', 'users.views.invalid_login', name='invalid'),
    url(r'^profile/(?P<user>[-\w]+)$', 'users.views.view_profile'   , name='user_profile'),
    url(r'add/$', views.AddMember.as_view(), name='profile-add'),
    url(r'^profile/adddetails/$',views.addMemberProfiledetails.as_view(), name='profiledetails-add' ),
    url(r'^updateprofile/(?P<pk>[0-9]+)/$', views.UserProfileUpdate.as_view(), name='profile-update'),
    url(r'deleteprofile/(?P<pk>[0-9]+)/delete/$', views.UserProfileDelete.as_view(), name='profile-delete'),
    url(r'^update_profile/$', 'users.views.update_profile', name='update_user_profile'),
    url(r'^your_profile/$', login_required(views.your_profile.as_view()), name='your_profile'),
    url(r'^dashboard', 'users.views.dashboard', name='dashboard'),
    url(r'^patient/$', 'users.views.patient_profile', name='patient_profile'),
    url(r'^patientvaccinedetails/$', 'users.views.patientvaccinedetails', name='patientvaccinedetails'),
    url(r'^vaccines', 'users.views.vaccinetype', name='vaccines'),
    url(r'^childvaccines', 'users.views.childvaccines',name='childvaccines'),
    url(r'^vaccinelist/$', 'users.views.vaccinelist', name='vaccinelist'),

    # Create, update, delete
    url(r'^newappointment', views.AppointmentCreateView.as_view(), name='new_appointment'),
    url(r'^editappointment/(?P<pk>[0-9]+)/edit$', views.AppointmentUpdateView.as_view(), name='edit_appointment'),
    url(r'^deleteappointment/(?P<pk>[0-9]+)/delete$', views.AppointmentDeleteView.as_view(), name='delete_appointment'),


    # List and detail views
            url(r'^viewappointments', views.AppointmentListView.as_view(), name='list_appointments'),
    url(r'^appointmentdetails/(?P<pk>[0-9]+)$', views.AppointmentDetailView.as_view(), name='view_appointment'),
    #url(r'^email/$', 'users.views.emaillist', name='emaillist'),

    # blog urls
    url(r'^blog/home$', 'users.views.index', name='blog_home'),
    url(r'^blog/view/(?P<slug>[^\.]+).html', 'users.views.view_post',  name='view_blog_post'),
    url(r'^blog/category/(?P<slug>[^\.]+).html',    'users.views.view_category',     name='blog_category'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)