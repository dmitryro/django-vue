from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager

class Category(models.Model):

    name = models.CharField(max_length=200,blank=True,null=True)
    code = models.CharField(max_length=200,blank=True,null=True)
    total_posts = models.IntegerField(default=0,blank=True,null=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)
# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=200,blank=True,null=True)
    link = models.CharField(max_length=700,blank=True,null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True,null=True) 
    author = models.ForeignKey(User,related_name='author',db_column="author",blank=True,null=True)  
    category = models.ForeignKey(Category,related_name='author',blank=True,null=True)
    is_archived = models.NullBooleanField(default=False,blank=True,null=True)
    is_flagged = models.NullBooleanField(default=False,blank=True,null=True)
    is_deleted = models.NullBooleanField(default=False,blank=True,null=True)
    is_published = models.NullBooleanField(default=False,blank=True,null=True)
    image = models.ImageField(upload_to='post_images',blank=True,null=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(100, 50)],
                                     format='JPEG',
                                     options={'quality': 60})

    total_comments = models.IntegerField(default=0,blank=True,null=True)
    tags = TaggableManager()

    @property
    def teaser(self):
        return self.body[0:600]

    @property
    def author_name(self):
        if not self.author:
           return 'some author'
        else:
           return self.author.first_name+' '+self.author.last_name

    def get_absolute_url(self):
        return '/'+self.title+'-'+self.category+'/'

#    @author.setter
#    def author(self, value):
#        self._author = value

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return "/posts/%i/" % self.id


class FilePost(models.Model):
    post = models.ForeignKey(Post, related_name='file_post', db_column="file_post", blank=True, null=True)
    file_name = models.CharField(max_length=1500,blank=True,null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=200,blank=True,null=True)

    class Meta:
        verbose_name = 'FilePost'
        verbose_name_plural = 'FilePosts'

    def __str__(self):
        return self.file_name


class Comment(models.Model):

    title = models.CharField(max_length=200,blank=True,null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=1500,blank=True,null=True)
    author = models.ForeignKey(User,related_name='comment_author',blank=True,null=True)
    post = models.ForeignKey(Post,related_name='post',blank=True,null=True)
    is_flagged = models.NullBooleanField(default=False,blank=True,null=True)
    is_deleted = models.NullBooleanField(default=False,blank=True,null=True)
    is_published = models.NullBooleanField(default=False,blank=True,null=True)
    is_anonymous = models.NullBooleanField(default=False,blank=True,null=True)
    avatar =  models.CharField(max_length=500,blank=True,null=True)
    username = models.CharField(max_length=200,blank=True,null=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return "/comments/%i/" % self.id


# Create your models here.
