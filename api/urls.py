from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parts.views import PartViewSet


router = DefaultRouter()


router.register(r'parts', PartViewSet, basename='part')


urlpatterns = [
    path('accounts/', include('rest_registration.api.urls')),
    path('v1/', include(router.urls)),

]