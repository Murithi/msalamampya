from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', 'users.views.home_page', name='home_page'),
    url(r'^user$', 'users.views.user_profile'   , name='user_profile'),
]