from django.urls import path
from .views import home, detail, new_post, create

urlpatterns = [
    path('', home, name='home'),
    path('<int:blog_id>', detail, name='detail'),
    path('new/', new_post, name='new'),
    path('create/', create, name='create'),
]