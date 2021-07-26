from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect as http
from django.http import JsonResponse
from django_user_agents.utils import get_user_agent
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models.signals import pre_save
from django.utils.crypto import get_random_string
from django.contrib.staticfiles.urls import static
import os
import re
import time
import json
from pprint import pprint
from .models import Food, Recipe, Plan, Inventory
from .forms import FoodForm, RecipeForm, PlanForm
from datetime import date


class IndexView(TemplateView):
	def get(self, request, *args, **kwargs):
		if request.method == 'GET':
			food = Food.objects.all()
			recipe = Recipe.objects.all()
		return render(request, 'index.html', context={'food': food, 'recipe': recipe})




class FoodView(TemplateView):
	def get(self, request, *args, **kwargs):
		if request.method == 'GET':
			form = FoodForm()
			food = Food.objects.all()

		return render(request, 'food_base.html', context={'form': form, 'food': food})

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			form = FoodForm(request.POST or None)

			if form.is_valid():
				name = form.cleaned_data['name']
				#sku = form.cleaned_data['sku']
				qty = form.cleaned_data['qty']
				ftype = form.cleaned_data['ftype']
				description = form.cleaned_data['description']
				cost = form.cleaned_data['cost']

				food = Food.objects.filter(name=name, ftype=ftype)
				if food:
					for item in food:
						item.name = name
						#item.sku = sku
						item.qty = qty
						item.ftype = ftype
						item.description = description
						item.cost = cost
						item.save()
						return http('/food_base/')

				else:
					f = Food.objects.create(name=name, qty=qty, ftype=ftype, description=description, cost=cost)
					return http('/food_base/')
			else:
				print(form.errors)
				return http('/food_base/')



class RecipeView(TemplateView):
	def my_choices(self):

		mychoices = Food.objects.all()
		choice = []
		cval = []
		for i in mychoices:
			choice.append(i.name)

		for m in mychoices:
			cval.append(m.id)
		zipped = zip(cval, choice)
		return list(zipped)
	def get(self, request, *args, **kwargs):
		if request.method == 'GET':

			form = RecipeForm()
			food = Food.objects.all()
			meat = Food.objects.filter(ftype='1')
			veggie = Food.objects.filter(ftype='2')
			spice = Food.objects.filter(ftype='3')
			recipe = Recipe.objects.all()
			mr = Recipe.objects.values('name')

			recipes = []

			for a in mr:
				for k, v in a.items():
					recipes.append(Recipe.objects.filter(name=v))

			print(recipes)
			#print(self.my_choices())
		return render(request, 'recipe_base.html', context={'form': form, 'recipe': recipe, 'myrecipe': recipes})

	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			rl = request.POST.getlist('extra_field_NaN')
			name = request.POST.get('name')
			description = request.POST.get('description')
			food = request.POST.get('name')
			form = RecipeForm(request.POST, extra=rl)
			foods = []

			if food is not None:
				foods.append(food)
			if rl is not None:
				for a in rl:
					foods.append(a)
			recipe = Recipe.objects.filter(name=name)
			if recipe.exists():
				for item in recipe:
					item.name = name
					item.food = foods
					item.description = description
					#item.cost = cost
					item.save()
				print('updated')
				return http('/recipe_base/')

			else:
				f = Recipe.objects.create(name=name, food=foods, description=description)
				print('created')
				return http('/recipe_base/')


class MyRecipe(TemplateView):

	def Convert(self, string):
		li = list(string.split(''))
		return li

	def get(self, request, pk, *args, **kwargs):
		thisrecipe = Recipe.objects.filter(pk=pk)
		mr = Recipe.objects.values('name')

		recipes = []
		ingredients = []
		for a in mr:
			for k, v in a.items():
				recipes.append(Recipe.objects.filter(name=v))
		for r in thisrecipe:
			x = str(r.food).replace('\"', '')
			y = re.findall(r'.*, ', x)
			z = str(y).replace('[', '')
			zed = str(z).replace(']', '')
			zedd = str(zed).replace('\n', '')
			for i in list((zedd.split(', '))):
				zee = str(i).strip('\'')
				for f in zee.split('\n'):
					if f != '':
						ingredients.append(f)

		return render(request, 'my_recipe.html', context={'myrecipe': recipes, 'thisrecipe': thisrecipe, 'ingredients': ingredients})

def json_plan(request):
	if request.method == 'GET':
		form = PlanForm()

		return render(request, 'plan_form.html', context={'form': form})
	else:
		if request.is_ajax():
			form = PlanForm(request.POST)
			print('is ajax')
			if form.is_valid():
				#print(request.POST)

				meal = request.POST.get('meal')
				day = request.POST.get('day')
				f = Plan.objects.create(meal=meal, day=day)
				return http('/plan_view/')
			print(form.errors)
		else:
			print('not ajax')
			form = PlanForm(request.POST)
			if form.is_valid():
				calendar = form.cleaned_data['calendar']
				for field in Plan.objects.all():
					field.calendar = calendar
					field.save()
				return http('/plan_view/')
			else:
				print(form.errors)


class PlanView(TemplateView):
	def get(self, request, *args, **kwargs):

		if request.is_ajax():
			pass
		else:
			form = PlanForm()
			recipe = Recipe.objects.all()
			recipes = []
			plan = Plan.objects.all()
			mr = Recipe.objects.values('name')
			for a in mr:
				for k, v in a.items():
					recipes.append(Recipe.objects.filter(name=v))
			title = []
			start = []
			myplans = []
			for a in plan:
				title.append(a.meal)
				start.append(a.day)
			z = zip(title, start)
			for x, y in list(z):

				myjson = {
					'title': x.replace('\"', ''),
					'start': y.replace('\"', ''),
					'end': 'null'
				}
				try:
					myplan = json.dumps(myjson, indent=4)
					myplans.append(myplan)
					print(myplans)
				except UnboundLocalError:
					pass
			try:
				return render(request, 'plan_base.html', context={'form': form, 'recipe': recipe, 'myrecipe': recipes, 'myplan': myplans})
			except UnboundLocalError:

				return render(request, 'plan_base.html', context={'form': form, 'recipe': recipe, 'myrecipe': recipes})






class KioskView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            today = date.today()
            print(today)
            inventory = Food.objects.all()
            recipe = Recipe.objects.all()
            try:
                for item in Plan.objects.all():
                    if str(today) == item.day.replace('\"', ''):
                        dinner = Plan.objects.filter(day=item.day)

                return render(request, 'kiosk_view.html', context={'inventory': inventory, 'dinner': dinner})
            except UnboundLocalError:
                dinner = 'No dinner plans!'

                return render(request, 'kiosk_view.html', context={'inventory': inventory, 'dinner': dinner})



