from http import HTTPStatus

from django.http import FileResponse
from rest_framework import permissions, response, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from core.views import parse_pricelist, parse_quotes_request, prepare_quotes
from inquiries.tasks import save_inquiry
from parts.models import Part
from parts.serializers import PartSerializer, PriceListSerializer
from parts.tasks import send_order
from plans.permissions import IsSupplier

from .permissions import IsOnPlanPermission


class ListRetrieveModelMixin(
    RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet
):
    pass


CHUNK_SIZE = 1000


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
            parsed_pricelist = parse_pricelist(pricelist_file)
        except Exception:
            return response.Response(
                {'detail': 'Ошибка обработки файла'},
                status=HTTPStatus.UNPROCESSABLE_ENTITY)
        Part.objects.all().delete()

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
            print(parsed_pricelist[0], flush=True)
            Part.objects.bulk_create(new_part_objs)

        return response.Response(data={'Файл получен'}, status=HTTPStatus.OK)

    @action(
        detail=False, methods=['post'],
        permission_classes=[IsOnPlanPermission]
    )
    def generate_quotes(self, request):
        """Наполняет файл с ценами и возвращает его."""
        try:
            quotes_request_file = request.FILES['quotes_request'].read()
        except Exception:
            raise ValidationError(
                detail={'file': 'Нужный файл не найден'},
                code=HTTPStatus.BAD_REQUEST)

        try:
            quote_requests = parse_quotes_request(quotes_request_file)
        except Exception:
            raise ValidationError(
                detail={'file': 'В файле содержатся ошибки'},
                code=HTTPStatus.BAD_REQUEST)

        save_inquiry.delay(quote_requests, request.user.pk)

        quotes = prepare_quotes(quote_requests, request.user)

        quotes.seek(0)

        with open(
            f'last_orders/{request.user.pk}_order.xlsx', 'wb+'
        ) as destination:
            destination.write(quotes.getbuffer())

        return FileResponse(
            quotes, as_attachment=True, filename='Quotes.xlsx')

    @action(
        detail=False, methods=['post'],
        permission_classes=[IsOnPlanPermission]
    )
    def place_order(self, request):
        """Отправляет поставщику заказ."""
        send_order.delay(
            seeker_pk=request.user.pk,
            seeker_entity=request.user.entity,
            seeker_email=request.user.email,
            seeker_phone_n=request.user.phone_number
        )
        return response.Response(
            data={'detail': 'Заказ отправлен'}, status=HTTPStatus.CREATED)
