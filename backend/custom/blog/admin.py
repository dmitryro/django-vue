from django.contrib import admin

from imagekit.admin import AdminThumbnail

from models import Post
from models import Comment
from models import Category
from models import FilePost
from ckeditor.widgets import CKEditorWidget
from wymeditor.models import WYMEditorField
from wymeditor.widgets import AdminWYMEditorArea
from forms import PostForm

# Register your models here.
class PostAdmin(admin.ModelAdmin):

    form = PostForm
    fieldsets = [
      ('Body', {'classes': ('full-width',), 'fields': ('title', 'category', 'body', 'author', 'image')})
    ]
    list_display = ('id','title','body','category','author_name','image_thumbnail','time_published')
    list_editable = ('title','category','body')
    image_thumbnail = AdminThumbnail(image_field='image_thumbnail')
    formfield_overrides = {
        WYMEditorField: {'widget': AdminWYMEditorArea},
    }


    class Meta:
         verbose_name = 'Post'
         verbose_name_plural = 'Posts'


class FilePostAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['post','file_name', 'author']}),)
    list_display = ('id','post','file_name','author')
    list_editable = ('file_name','author',)

    class Meta:
         verbose_name = 'File Post'
         verbose_name_plural = 'File Posts'
    

class CommentAdmin(admin.ModelAdmin):

    fieldsets = ((None, {'fields': ['post','title','body','author']}),)
    list_display = ('id','title','body','author')
    list_editable = ('title','body')

    class Meta:
         verbose_name = 'Comment'
         verbose_name_plural = 'Comments'


class CategoryAdmin(admin.ModelAdmin):

    fieldsets = ((None, {'fields': ['name','code']}),)
    list_display = ('id','name','code')
    list_editable = ('name','code')

    class Meta:
         verbose_name = 'Category'
         verbose_name_plural = 'Categories'


admin.site.register(FilePost, FilePostAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
