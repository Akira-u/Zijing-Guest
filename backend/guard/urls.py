from django.urls import path,include 
from rest_framework.routers import DefaultRouter
import guard.views as views

app_name = 'guard'

router = DefaultRouter()
router.register(r'log', views.LogViewSet)
urlpatterns = [
    path('',include(router.urls)),
]

