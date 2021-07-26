
from django.contrib import admin
from django.urls import path
from . import views
from . import static
from . import forms
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('food_base/', views.FoodView.as_view(), name='food_view'),
    path('recipe_base/', views.RecipeView.as_view(), name='recipe_view'),
    path('recipe_base/<int:pk>/', views.MyRecipe.as_view(), name='my_recipe'),
    path('plan_base/', views.PlanView.as_view(), name='plan_view'),
    path('plan_view/', views.json_plan, name='json_plan'),
    path('kiosk_view/', views.KioskView.as_view(), name='kiosk_view'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
