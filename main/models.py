from django.db import models
from django.utils.text import slugify

from django.db.models.signals import pre_save
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from multiselectfield import MultiSelectField

#Walmart API key
#37B78AE7FD974487AC9E863F1D45265D

choices = (
    ('1', 'Meat'),
    ('2', 'Veggie'),
    ('3', 'Spice')
)



#import requests
#
## set up the request parameters
#params = {
#  'api_key': '37B78AE7FD974487AC9E863F1D45265D',
#  'type': 'search',
#  'customer_zipcode': '77001',
#  'search_term': 'highlighter pens',
#  'category_id': '1229749'
#}
#
## make the http GET request to BlueCart API
#api_result = requests.get('https://api.bluecartapi.com/request', params)
#
## print the JSON response from BlueCart API
#print(json.dumps(api_result.json()))




class Food(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    sku = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    ftype = models.CharField(max_length=200, null=True, blank=True, choices=choices)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=5, decimal_places=2, null=True)


    def __str__(self):
        return self.name


def my_choices():

    mychoices = Food.objects.all()


    choice = []
    cval = []
    for i in mychoices:
        choice.append(i.name)

    for m in mychoices:
        cval.append(m.id)
    zipped = zip(cval, choice)

    return list(zipped)


class Recipe(models.Model):
    food = models.CharField(max_length=50000, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    #cost = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    description = HTMLField(null=True, blank=True)


    slug = models.SlugField(unique=False, null=True, blank=True)
    def __str__(self):
        return self.name

    #def save(self):
        #for item in Food.objects.all():
            #item+item+item  etc..

        #super(Recipe, self).save():
        #return
day_choices = (
    ('1', 'Sunday'),
    ('2', 'Monday'),
    ('3', 'Tuesday'),
    ('4', 'Wednesday'),
    ('5', 'Thursday'),
    ('6', 'Friday'),
    ('7', 'Saturday'),
    )

class Plan(models.Model):
    week = models.CharField(max_length=10, null=True, blank=True)
    day = models.CharField(max_length=50, null=True, blank=True)
    meal = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):

        return "{} - {}".format(self.meal, self.day)


class Inventory(models.Model):
    total = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.total.sku







def create_recipe_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)


    return slug

def pre_save_Recipe_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_recipe_slug(instance)



pre_save.connect(pre_save_Recipe_receiver, sender=Recipe)

