from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics

from models import Category
from models import Post
from models import Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')
    

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id','name','code')


class PostSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=False,read_only=True)
    author = UserSerializer(many=False,read_only=True)
     
    class Meta:
        model = Post
        fields = ('id','author','title','time_published','category',
                  'body','link','image','total_comments','teaser')

class CommentSerializer(serializers.ModelSerializer):

    post = PostSerializer(many=False,read_only=True)
   
    class Meta:
        model = Comment
        fields = ('id','title','body','author','post','avatar','is_anonymous','username')
