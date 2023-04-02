from rest_framework import viewsets, permissions, response
from rest_framework.decorators import action
from parts.models import Part
from parts.serializers import PartSerializer, PriceListSerializer
from http import HTTPStatus
from datetime import datetime as dt
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin


class ListRetrieveModelMixin(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    pass

class PartViewSet(ListRetrieveModelMixin):
    queryset = Part.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'post':
            return PriceListSerializer
        return PartSerializer
    
    @action(detail=False, methods=['post'])
    def add_parts(self, request):
        parsed_pricelist = Part.get_parts(request.FILES['pricelist'])
        chunks_total = len(parsed_pricelist) // 5000
        time1 = dt.now()

        for i in range(chunks_total):
            creation_data = [Part(
                name=row['description'],
                uid=row['article_'],
                initial_price=row['netprice_dso']
            ) for row in parsed_pricelist[i*1000:(i+1)*1000]]
            Part.objects.bulk_create(creation_data)

            if i + 1 == chunks_total:
                creation_data = [Part(
                    name=row['description'],
                    uid=row['article_'],
                    initial_price=row['netprice_dso']
                ) for row in parsed_pricelist[(i+1)*1000:]]
                Part.objects.bulk_create(creation_data)


        time2 = dt.now()
        print(time2 - time1)
        time3 = dt.now()
        print(time3 - time2)
        return response.Response(data={'Файл получен'}, status=HTTPStatus.OK)

