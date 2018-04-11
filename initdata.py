

#data list format is "xxx - ab " xxx is menu name and  ab is category a,b

#import django project's settings.py

import os
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant.settings")
from django.conf import settings
from django.core.management import execute_from_command_line as ecl
import django
django.setup()
from food import models

f="data/data.txt"
f=open(f,"r")
category_list = {
        'f':"fried",
        's':"soup/curry",
        'w':"seafood",
        'c':"chicken",
        'p':"pork",
        'v':"vegetable",
        'x':"salad",
        '1':"drink",
        'r':"rice",
        }
dl=f.readlines()

#split xxx - ab to [xx,ab]
dl = [i.split("-") for i in dl]

#split [xxx,ab] to [xxx,[a,b]] and remove "\n" and " " at end
dl = map(lambda x :(x[0].strip(),[i for i in x[1][:-1] if i is not " "]), dl)



if __name__=="__main__":

    #delete every entry in database
    _ = [x.delete() for x in models.FoodCategory.objects.all()]
    _ = [x.delete() for x in models.MenuItem.objects.all()]

    category={}
    for x in category_list:
        category[x]=models.FoodCategory.objects.create(name=category_list[x])

    print(category)
    for x in dl:
        menu =models.MenuItem.objects.create(name = x[0], price = random.randrange(1,9)*900)
        for i in x[1]:
#            print(category[i])
            #print(x[1])
            menu.category.add(category[i])


