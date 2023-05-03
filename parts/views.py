from http import HTTPStatus

from django.http import FileResponse
from rest_framework import permissions, response, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from core.views import parse_quotes_request, prepare_quotes
from parts.models import Part
from parts.serializers import PartSerializer, PriceListSerializer
from plans.permissions import IsSupplier

from .permissions import IsOnPlanPermission
from parts.tasks import add


class ListRetrieveModelMixin(
    RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet
):
    pass


class PartViewSet(ListRetrieveModelMixin):
    queryset = Part.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'post':
            return PriceListSerializer
        return PartSerializer

    @action(
            detail=False, methods=['post'],
            permission_classes=[IsSupplier])
    def add_parts(self, request):
        """Добавляет в БД запчасти из файла."""
        pricelist_file = request.FILES['pricelist'].read()
        try:
            parsed_pricelist = Part.get_parts(pricelist_file)
        except Exception:
            return response.Response(
                {'detail': 'Ошибка обработки файла'},
                status=HTTPStatus.UNPROCESSABLE_ENTITY)
        Part.objects.all().delete()

        CHUNK_SIZE = 1000
        chunks_amount = len(parsed_pricelist) // CHUNK_SIZE

        for i in range(chunks_amount):
            if i == chunks_amount - 1:
                new_part_objs = (Part(**obj) for obj in parsed_pricelist[
                    i*CHUNK_SIZE:len(parsed_pricelist)
                ])
                Part.objects.bulk_create(new_part_objs)
                break
            new_part_objs = (
                Part(**obj) for obj in parsed_pricelist[
                    i*CHUNK_SIZE:(i+1)*CHUNK_SIZE
                ]
            )
            Part.objects.bulk_create(new_part_objs)

        return response.Response(data={'Файл получен'}, status=HTTPStatus.OK)

    @action(
        detail=False, methods=['post'],
        permission_classes=[IsOnPlanPermission]
    )
    def generate_quotes(self, request):
        """Наполняет файл с ценами и возвращает его."""
        quotes_request_file = request.FILES['quotes_request'].read()
        try:
            quote_requests = parse_quotes_request(quotes_request_file)
        except Exception:
            return response.Response(
                {'detail': 'Ошибка обработки файла'},
                status=HTTPStatus.UNPROCESSABLE_ENTITY)
        quotes = prepare_quotes(quote_requests, request.user)

        quotes.seek(0)
        r = add.delay(1,110)
        print(r.get())
        return FileResponse(quotes, as_attachment=True, filename='Quotes.xlsx')
