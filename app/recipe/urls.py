from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'recipe'

router = DefaultRouter()
router.register('tag', views.TagViewSet, basename='tag')
router.register('ingridient', views.IngridientViewSet, basename='ingridient')
router.register('recipe', views.RecipeViewSet, basename='recipe')

urlpatterns = router.urls
