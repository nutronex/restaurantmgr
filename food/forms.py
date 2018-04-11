
from django.forms import ModelForm
from .models import MenuItem, FoodCategory,Order
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CheckboxSelectMultiple


class CustomAuthForm(AuthenticationForm):
    def __init__(self,*a,**ka):
        super(CustomAuthForm,self).__init__(*a,**ka)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})



class BootstrapFormMixin(object):
    """ this mixin add input's class 'form-control'  from bootstrap """
    def __init__(self,*a,**ka):
        super(BootstrapFormMixin,self).__init__(*a,**ka)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})




class MenuItemForm(ModelForm):
    def __init__(self,*a,**ka):
        super(MenuItemForm,self).__init__(*a,**ka)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
        #self.fields['category'].widget.attrs = {'class':'foo'}
        #self.fields['category'].label_classes= ('shit',)

    class Meta:
        model = MenuItem
        fields =  ['name','description','category','price','image']
        widgets = {
        #        'category':CheckboxSelectMultiple()
                }

class OrderForm(ModelForm):
    def __init__(self,*a,**ka):
        super(OrderForm,self).__init__(*a,**ka)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
    class Meta:
        model = Order
        fields = ['item','quantity','table','parcle']


class FoodCategoryForm(ModelForm):

    def __init__(self,*a,**ka):
        super(FoodCategoryForm,self).__init__(*a,**ka)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = FoodCategory
        fields = ['name',]

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
class AccountForm(forms.Form):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20,widget=forms.widgets.PasswordInput,label="Password")
    password2 = forms.CharField(max_length=20,widget=forms.widgets.PasswordInput,label="confirm password")



    def __init__(self,*a,**ka):
        super(AccountForm,self).__init__(*a,**ka)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
            self.fields[i].help_text =  ''


