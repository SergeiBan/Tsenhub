from rest_framework import viewsets
from plans.models import Plan
from plans.serializers import PlanSerializer, UsersPlanSerializer
from plans.permissions import IsSupplier
from django.contrib.auth import get_user_model
from rest_framework import response


User = get_user_model()


class PlanViewSet(viewsets.ModelViewSet):
    """Все операции с тарифами разрешены поставщикам."""
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    pagination_class = None
    permission_classes = [IsSupplier]


class UpdateUsersPlanViewSet(viewsets.ViewSet):
    """Изменяет скидочный тариф любому числу клиентов. Разрешено поставщику."""
    permission_classes = [IsSupplier]

    def create(self, request):
        serializer = UsersPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        users_pks = serializer.data['users']
        plank_pk = serializer.data['plan']
        User.objects.filter(
            id__in=users_pks
        ).update(plan=plank_pk)

        return response.Response({'update': 'success'})