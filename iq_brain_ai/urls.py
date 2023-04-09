"""iq_brain_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from app.authentication.views.api_views import UserViewSet, GroupViewSet, PermissionViewSet
from app.core.views.api_views import QuestionsList, StatsList, ComposeQuestion

urlpatterns = [
    path(r'', include('app.authentication.urls'), name='auth'),
    path('admin/', admin.site.urls),
    #path('polls/', include('app.core.urls'))
]

#for REST API auto binding
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns += [
    path(r'auth/', include((router.urls, 'iq-brainer'), namespace='authAPI')),
    path(r'auth/token', obtain_auth_token, name='api_token_auth'),
]

router = routers.DefaultRouter()

router.register(r'question', QuestionsList)

urlpatterns += [
    path(r'api/', include((router.urls, 'iq-brainer'), namespace='api')),
    path(r'api/getQ', ComposeQuestion.as_view(), name="api"),
    path(r'api/stats', StatsList.as_view({'get': 'list'}), name="stats"),
]

schema_view = get_schema_view(
    openapi.Info(
        title="IQ Brainer",
        default_version='v1',
        description="An IQ test app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated, ],
)

urlpatterns += [
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
