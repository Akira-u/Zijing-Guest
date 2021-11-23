from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
import guard.views as views

app_name = 'guard'

router = DefaultRouter()
router.register(r'log', views.LogViewSet)
router.register(r'guest', views.GuestViewSet)
router.register(r'guard',views.GuardViewSet)

urlpatterns = [
    path('',include(router.urls)),
]



