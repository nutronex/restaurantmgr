from django.contrib import admin

from .models import FoodCategory,MenuItem

class FoodCategoryAdmim(admin.ModelAdmin):

    pass

admin.site.register(FoodCategory,FoodCategoryAdmim)


class FoodCategoryTabular (admin.TabularInline):
    model =  MenuItem.category.through


class MenuItemAdmim(admin.ModelAdmin):
    """m2m field is not supported in list_display so add method name
       model instance is passed to instance method x(self,obj)"""

    list_display = ('name','description','category_list','price','image')
#    inlines = [FoodCategoryTabular,]
#    exclude = ('',)

    def category_list(self,obj):
        return ' | '.join(x.name for x in obj.category.all())


    #fields = ('name','category','price')
    #fields is for update/add page

admin.site.register(MenuItem,MenuItemAdmim)


# Register your models here.
