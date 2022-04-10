from rest_framework import serializers
from core import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'

class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingridient
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):

    ingridients = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Ingridient.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Tag.objects.all())
    class Meta:

        model = models.Recipe
        fields = ['id','user','title','time_minutes','price','link','ingridients','tags']
        read_only_fields = ['id']

class RecipeDetailSerializer(RecipeSerializer):

    ingridients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)