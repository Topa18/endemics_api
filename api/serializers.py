from rest_framework import serializers
from .models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
        extra_kwargs = {
            'scientific_name': {'required': False},
            'common_name': {'required': False},
            'group': {'required': False},
            'conservation_status': {'required': False},
            'image': {'required': False}
        }


class AnimalCountQuerySerializer(serializers.Serializer):
    count = serializers.IntegerField(
        default=1,
        min_value=1,
        max_value=5
    )