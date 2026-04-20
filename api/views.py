from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status

from dotenv import load_dotenv
import requests
import os

from .models import Animal
from.serializers import AnimalSerializer, AnimalCountQuerySerializer


tags = ['Species']

class AnimalView(GenericAPIView, ListModelMixin, DestroyModelMixin):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    @extend_schema(
            summary="Get endemics list",
            description="Endpoint allows user to get list of all collected species",
            tags=tags
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
            summary='Collect new species',
            description="Allows user to collect new species" \
            "from external API",
            tags=tags,
            request=AnimalCountQuerySerializer,
            parameters=[
                OpenApiParameter(
                    name='count',
                    location=OpenApiParameter.QUERY,
                    description='Specifies how many objects, request receives',
                    required=False,
                    default=1,
                    type=int
                )
            ]
    )
    def post(self, request, *args, **kwargs):
        query_serializer = AnimalCountQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        count = query_serializer.validated_data['count']

        existing_names = set(self.get_queryset().values_list('common_name', flat=True))
        tries = 0
        tries_limit = count * 2
        spieces_count = self.max_requests()

        if len(existing_names) == spieces_count:
            return Response(data={'message': 'All spieces collected'},
                            status=status.HTTP_204_NO_CONTENT)

        collected_data = []
        while len(collected_data) < count:
            
            load_dotenv()
            try:
                r = requests.get(url=os.getenv("URL"), timeout=10)
            except requests.RequestException as e:
                return Response(data={'error': 'External API Error. Try again later '},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            source_data = r.json()
            serializer = self.get_serializer(data=source_data)
            if serializer.is_valid():
                new_data = serializer.validated_data.get('common_name')
                if new_data in existing_names:
                    print(f'{new_data} exists!')       # LOG!
                    tries += 1
                    if tries >= tries_limit:
                        if not collected_data:
                            return Response(data={'data': collected_data,
                                                  'message': 'Cooldown. Try again later.',
                                                  'count': f'Own data: {len(existing_names)}/External data: {spieces_count}'}, 
                                            status=status.HTTP_204_NO_CONTENT)
                        return Response(data={'data': collected_data,
                                              'message': f'Collected {len(collected_data)}/{count}. Cooldown. Try again later',
                                              'count': f'Own data: {len(existing_names)}. External data: {spieces_count}'},
                                        status=status.HTTP_206_PARTIAL_CONTENT)
                    continue

                serializer.save()
                collected_data.append(serializer.data)

        return Response(data={'data': collected_data,
                              'message': f'{tries} coincedence occured. '\
                                         f'{len(collected_data)}/{count} objects collected',
                              'count': f'Own data: {len(existing_names)}. External data: {spieces_count}'},
                        status=status.HTTP_201_CREATED)

    @extend_schema(
            summary="Clear all species data",
            description="Allows user to delete all species in own DB",
            tags=tags,
            operation_id='animal_clear'
    )
    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for obj in queryset:
            obj.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT) 
    
    def max_requests(self):
        try:
            r = requests.get(url=os.getenv('MAX_URL'), timeout=10)
            data = r.json()
            return data.get('count')
        except requests.RequestException as e:
            return Response(data={'error': 'External API Error. Try again later '},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnimalDetailView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    @extend_schema(
            summary="Get species by ID",
            description="Allows users to retrieve current species by it`s ID",
            tags=tags
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete species by ID",
        description="Allows users to delete current species by it`s ID",
        tags=tags
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

