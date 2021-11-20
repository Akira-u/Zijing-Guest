"""ZijingGuest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import views

router = routers.DefaultRouter()
router.register('api_info', views.APIInfoViewSet)
schema_view = get_schema_view(
    openapi.Info(
        title="测试工程API",
        default_version='v1.0',
        description="测试工程接口文档",
        terms_of_service="#",
        contact=openapi.Contact(email="测试"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('visitor/', include('visitor.urls',namespace='visitor')),
    path('guard/', include('guard.urls',namespace='guard')),
    path('admin/', admin.site.urls),
     # 配置django-rest-framwork API路由
    url('api/', include('api.urls')),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 配置drf-yasg路由
    url('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]