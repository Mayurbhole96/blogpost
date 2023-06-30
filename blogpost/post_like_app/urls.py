from django.urls import include, path
from rest_framework import routers
# from django.urls.conf import re_path
from . import views
from .views import (
    LikeListView,
    LikeCreateView,
    LikeDestroyView,
)

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('api/posts/<int:pk>/likes/', LikeCreateView.as_view(), name='like_create'),
    path('posts/<int:pk>/likes/', LikeListView.as_view(), name='like-list'),
    path('api/posts/<int:pk>/likes/<int:user_id>/', LikeDestroyView.as_view(), name='like_destroy'),
    path('', include(router.urls)),    
]
