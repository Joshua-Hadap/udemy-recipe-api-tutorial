from rest_framework import serializers
from core import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'