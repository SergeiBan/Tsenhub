from django.contrib.auth import get_user_model
from rest_framework import response, status, viewsets
from rest_framework.decorators import action

from plans.models import Plan
from plans.permissions import IsSupplier
from plans.serializers import (PlanSerializer, RemovePlansSerializer,
                               UsersPlanSerializer)

User = get_user_model()


class PlanViewSet(viewsets.ModelViewSet):
    """Все операции с тарифами разрешены поставщикам."""
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    pagination_class = None
    permission_classes = [IsSupplier]

    @action(['DELETE'], detail=False)
    def remove_plans(self, request):
        """Поставщик удаляет любое число тарифов."""
        serializer = RemovePlansSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        pks = serializer.validated_data['plans']
        selected_plans = Plan.objects.filter(pk__in=pks)
        if selected_plans:
            selected_plans.delete()
        response_data = PlanSerializer(Plan.objects.all(), many=True).data
        return response.Response(
            response_data, status=status.HTTP_200_OK)


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

        return response.Response(
            {'update': 'success'}, status=status.HTTP_200_OK)
