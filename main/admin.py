from django.contrib import admin
from .models import Food, Recipe, Plan, Inventory

mmodels = []
mmodels.append([Food, Recipe, Plan, Inventory])
for m in mmodels:
    admin.site.register(m)

