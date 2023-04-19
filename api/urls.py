from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parts.views import PartViewSet
from users.views import UserViewSet, PlanViewSet


router = DefaultRouter()


router.register(r'parts', PartViewSet, basename='part')
router.register(r'users', UserViewSet, basename='user')
router.register(r'plans', PlanViewSet, basename='plan')


urlpatterns = [
    path('accounts/', include('rest_registration.api.urls')),
    path('v1/', include(router.urls)),
]
