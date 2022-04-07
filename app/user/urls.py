from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'user'

router = DefaultRouter()
router.register('user', views.CreateUserViewSet, basename='user')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'login/', views.LoginView.as_view(), name='login')
]
