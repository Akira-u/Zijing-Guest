from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.APIList.as_view()),
    url('<int:pk>/', views.APIDetail.as_view()),
]