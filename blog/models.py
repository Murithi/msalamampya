from django.db import models
from django.db.models import permalink

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=500, unique=True)
    intro = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('blog.Category')
    image = models.ImageField(upload_to="images/", null=True)
    imagecredit = models.CharField(max_length=100, unique=True)
    imagecaption = models.CharField(max_length=100, unique=True)
    timestamp= models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, { 'slug': self.slug })