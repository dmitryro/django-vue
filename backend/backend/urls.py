"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_swagger.views import get_swagger_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from chat.views import direct_chat_view, group_chat_view
from users.views import UserListView, CreateUserView, auth_user

schema_view = get_swagger_view(title='Pastebin API')



urlpatterns = [
    path('auth/', auth_user),
    path('direct/', direct_chat_view),
    path('group/', group_chat_view),
    path('register/', CreateUserView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserListView.as_view()),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
    path('docapi', schema_view),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
