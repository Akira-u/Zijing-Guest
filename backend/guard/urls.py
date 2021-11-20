from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
import guard.views as views

app_name = 'guard'

router = DefaultRouter()
router.register(r'log', views.LogViewSet)
router.register(r'guest', views.GuestViewSet)
router.register(r'guard',views.GuardViewSet)
router.register(r'test1',views.Test1ViewSet)
router.register(r'test2',views.Test2ViewSet)
urlpatterns = [
    path('',include(router.urls)),
]



