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
from.serializers import AnimalSerializer


class AnimalView(GenericAPIView, ListModelMixin):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        load_dotenv()
        try:
            r = requests.get(url=os.getenv("URL"), timeout=10)
        except requests.RequestException as e:
            return Response(data={'error': 'External API Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        source_data = r.json()
        serializer = self.get_serializer(data=source_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnimalDetailView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

