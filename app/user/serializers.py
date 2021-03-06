from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email','name','password']
        extra_kwargs = {'password': {'write_only': True, 'min_length':5}}