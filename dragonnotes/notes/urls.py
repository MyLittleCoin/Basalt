from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet) 
#router.register(r'projects', views.ProjectViewApi)
urlpatterns = [
    path('', include(router.urls)),
    path('myprojects/', views.ProjectViewApi.as_view()),
    path('myprojects/download', views.ProjectDownload.as_view()),
    path('myprojects/upload', views.FileView.as_view()),
]