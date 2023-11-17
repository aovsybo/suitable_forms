from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import DestroyAPIView, RetrieveAPIView, ListAPIView

from .models import Form
from .serializers import FormSerializer
from .service import get_types, convert_data


class FormAPI(APIView):
    def post(self, request, *args, **kwargs):
        data_types = get_types(request.data)
        query = Q()
        for key, value in data_types.items():
            query &= Q(fields={key: value})
        queryset = Form.objects.filter(query).first()
        if not queryset:
            return Response(data_types, status=status.HTTP_200_OK)
        form_serializer = FormSerializer(queryset)
        form_name = convert_data(form_serializer.data)["name"]
        return Response(form_name, status=status.HTTP_200_OK)


class CreateFormAPI(APIView):
    def post(self, request, *args, **kwargs):
        form_serializer = FormSerializer(data=request.data)
        if form_serializer.is_valid():
            form_serializer.save()
            return Response(form_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
