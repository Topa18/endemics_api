from django.shortcuts import render
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


class AnimalView(GenericAPIView, ListModelMixin, DestroyModelMixin):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        query_serializer = AnimalCountQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        count = query_serializer.validated_data['count']

        own_data = self.get_queryset()
        tries = 0

        collected_data = []
        while len(collected_data) < count:
            load_dotenv()
            retry = 0
            try:
                r = requests.get(url=os.getenv("URL"), timeout=10)
            except requests.RequestException as e:
                return Response(data={'error': 'External API Error. Try again later '}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            source_data = r.json()
            serializer = self.get_serializer(data=source_data)
            if serializer.is_valid():
                for data in own_data:
                    if data.common_name == serializer.validated_data.get('common_name'):

                        # LOG
                        print('exists!')
                        print(serializer.validated_data.get('common_name'))
                        # LOG

                        retry = 1
                        tries += 1
                        break
                if tries >= 15:
                    return Response(data={'message': 'All spieces collected (> 15 coincedences)'}, 
                                    status=status.HTTP_204_NO_CONTENT)
                if retry:
                    continue            

                serializer.save()
                collected_data.append(serializer.data)
        return Response(collected_data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for obj in queryset:
            obj.delete()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT) 


class AnimalDetailView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

