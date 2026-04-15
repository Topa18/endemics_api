from django.urls import path
from api.views import AnimalView, AnimalDetailView


urlpatterns = [
    path('', AnimalView.as_view(), name='animal_list'),
    path('<int:pk>/', AnimalDetailView.as_view(), name='animal_detail')
]
