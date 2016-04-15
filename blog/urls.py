from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from blog import views

urlpatterns = [
url(r'^blog/home$', 'blog.views.index'),
url(r'^blog/view/(?P<slug>[^\.]+).html', 'blog.views.view_post',  name='view_blog_post'),
url(r'^blog/category/(?P<slug>[^\.]+).html',    'blog.views.view_category',     name='view_blog_category'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)