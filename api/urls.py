from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from parts.views import PartViewSet
from plans.views import PlanViewSet, UpdateUsersPlanViewSet
from users.views import CustomTokenObtainPairView, UserViewSet

router = DefaultRouter()


router.register(r'parts', PartViewSet, basename='part')
router.register(r'users', UserViewSet, basename='user')
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'usersplan', UpdateUsersPlanViewSet, basename='usersplan')


urlpatterns = [
    path(
        'token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router.urls)),
]
