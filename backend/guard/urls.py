from django.urls import path,include 
from rest_framework.routers import DefaultRouter
import guard.views as views

app_name = 'guard'

router = DefaultRouter()
router.register(r'log', views.LogViewSet)
router.register(r'user', views.UserViewSet)
urlpatterns = [
    path('',include(router.urls)),
]

