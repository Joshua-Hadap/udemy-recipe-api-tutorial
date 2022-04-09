from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from core import models
from .serializers import TagSerializer


# Create your views here.

class TagViewSet(viewsets.ModelViewSet):

    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Tag.objects.filter(user=self.request.user).order_by('-name')