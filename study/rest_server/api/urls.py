from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostViewset, MemeberViewset


post_list = PostViewset.as_view({
    'post': 'create',
    'get': 'list'
})

post_detail = PostViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

member_list = MemeberViewset.as_view({
    'post': 'create',
    'get': 'list'
})

member_detail = MemeberViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:pk>', post_detail, name='post_detail'),
    path('members/', member_list, name='member_list'),
    path('members/<int:pk>', member_detail, name='member_detail')
])