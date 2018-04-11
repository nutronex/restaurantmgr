from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.shortcuts import render
from django.views.generic import  ListView,DetailView,CreateView ,UpdateView,FormView
from django.views.generic.dates import DayArchiveView
from django.views.generic import DeleteView
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from .models import Order,BillId,MenuItem, FoodCategory
from .forms import MenuItemForm , FoodCategoryForm,OrderForm
from .serializers import OrderSerializerVerbose
from .serializers import OrderSerializer
from .mixins import AjaxMixin
import os

def index_view(request):
    return render(request,'index.html',{'form':FoodCategoryForm()})

class MakeOrderMixix(object):
    model = Order
    form_class = OrderForm
    template_name = 'food/order_form.html'
    success_url = '/order/pending'

class MakeOrderUpdateView(MakeOrderMixix,LoginRequiredMixin,UpdateView):
    @method_decorator(csrf_exempt,login_required)
    def dispatch(self,req,*a,**ka):
        return super(MakeOrderUpdateView,self).dispatch(req,*a,**ka)


class MakeOrderDeleteView(MakeOrderMixix,LoginRequiredMixin,DeleteView):
    @method_decorator(csrf_exempt,login_required)
    def dispatch(self,req,*a,**ka):
        return super(MakeOrderDeleteView,self).dispatch(req,*a,**ka)

from django.shortcuts import redirect
class MakeOrderCreateView(MakeOrderMixix,LoginRequiredMixin,CreateView):

    def post(self,request,*args,**kwargs):
        """ here i hv to override post for printing some shit stuff"""
        form = self.get_form()
        if form.is_valid() :
            #print(type(form.cleaned_data["quantity"]))
            if form.cleaned_data['quantity']<=0:
                print("quantity is zero")
                return redirect("/order/pending")
                #return HttpResponseRedirect("/pending")
            to_print =[]
            printitem=[
            form.cleaned_data["item"].name,
            form.cleaned_data["quantity"],
            form.cleaned_data["table"]]

            print(to_print)
            if form.cleaned_data["parcle"] :
                printitem[0] += "(p)"
            to_print.append(printitem)
            to_print = str(to_print)
            os.system(os.getcwd()+"\\ConsoleApplication1\\ConsoleApplication1\\bin\\Debug\\ConsoleApplication1.exe"+" "+str(to_print))
        return super(MakeOrderCreateView,self).post(request,*args,**kwargs)


    @method_decorator(csrf_exempt,login_required)
    def dispatch(self,req,*a,**ka):
        return super(MakeOrderCreateView,self).dispatch(req,*a,**ka)






class FoodCategoryCreateView(LoginRequiredMixin,AjaxMixin,CreateView):
    model = FoodCategory
    form_class = FoodCategoryForm
    template_name = 'food/foodcategory_form_add.html'
    success_url = '/foodcategory/'
    @method_decorator(csrf_exempt,login_required)
    def dispatch(self,req,*a,**ka):
        return super(FoodCategoryCreateView,self).dispatch(req,*a,**ka)

class MenuItemCreateView(LoginRequiredMixin,AjaxMixin,CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name= 'food/menuitem_form.html'
    @method_decorator(csrf_exempt)
    def dispatch(self,req,*a,**ka):
        return super(MenuItemCreateView,self).dispatch(req,*a,**ka)

class FoodCategoryDetailView(LoginRequiredMixin,DetailView):
    model = FoodCategory

from django.views.generic import View
from django.http import JsonResponse

class FoodCategoryListView(LoginRequiredMixin,ListView,AjaxMixin):
    model = FoodCategory
    @method_decorator(csrf_exempt)
    def dispatch(self,req,*a,**ka):
        return super(FoodCategoryListView,self).dispatch(req,*a,**ka)

    def get_context_data(self,**kwargs):
        x = super(FoodCategoryListView,self).get_context_data(**kwargs)
        x.update({'form':FoodCategoryForm()})
        return x


class FoodCategoryDeleteView(LoginRequiredMixin,DeleteView):
    model = FoodCategory
    success_url='/foodcategory/'
    @method_decorator(csrf_exempt)
    def dispatch(self,req,*a,**ka):
        return super(FoodCategoryDeleteView,self).dispatch(req,*a,**ka)



class MenuItemDeleteView(LoginRequiredMixin,DeleteView):
    model = MenuItem
    success_url='/menu/'
    @method_decorator(csrf_exempt)
    def dispatch(self,req,*a,**ka):
        return super(MenuItemDeleteView,self).dispatch(req,*a,**ka)

class MenuItemUpdateView(LoginRequiredMixin,UpdateView,AjaxMixin):
    model = MenuItem
    success_url='/menu/'
    form_class = MenuItemForm
    @method_decorator(csrf_exempt)
    def dispatch(self,req,*a,**ka):
        return super(MenuItemUpdateView,self).dispatch(req,*a,**ka)

class FoodCategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = FoodCategory
    success_url='/foodcategory/'
    form_class = FoodCategoryForm


class MenuItemCreateView(LoginRequiredMixin,CreateView):
    model = MenuItem
    success_url='/menu/'
    form_class = MenuItemForm
    @method_decorator(login_required,csrf_exempt)
    def dispatch(self,req,*a,**ka):
        print("menuitem create view")
        return super(MenuItemCreateView,self).dispatch(req,*a,**ka)



class MenuItemListView(View):
    """ view for menuitem when http method is get it return list of menu and form
         and then handle for ajax request via post method """

    form_class = MenuItemForm
    template_name = 'food/menuitem_list.html'

    def get(self,request):
        menuitemlist = MenuItem.objects.all()
        return render(request,self.template_name,{'object_list':menuitemlist,'form':self.form_class()})

    @method_decorator(login_required)
    def post(self,request):
        data =  dict(request.POST)
        data.update({'category':[request.POST['category[]']]})
        data.update({'price':request.POST['price'][0]})
        data.update({'name':request.POST['name']})
        data.update({'image':request.POST['image']})
        data = self.form_class(data)

        if data.is_valid():
            data.save()
            return JsonResponse({'status':'saved successfully','name':data.cleaned_data['name']})
        else :
            data=dict(data.errors)
            return JsonResponse(data)

    @method_decorator(login_required,csrf_exempt)
    def dispatch(self,req,*a,**ka):
        return super(MenuItemListView,self).dispatch(req,*a,**ka)


@login_required
def menu_item_update_mini_view(request,pk):
    """ this view handle menuitem's  locked or favourite  state ,request come from menuitem_listview """

    if request.method=='POST':
        try:
            data=MenuItem.objects.get(pk=pk)
            fav=request.POST.get('favourite',None)
            lock=request.POST.get('locked',None)
            returndata={'status':200,'pk':pk}
            if fav :
                data.favourite=True if fav=="0" else False
                returndata.update({'val':data.favourite})
            if lock :
                data.locked=True if lock=="0" else False
                returndata.update({'val':data.locked})
            data.save()

            return JsonResponse(returndata)
        except MenuItem.DoesNotExist:
            return JsonResponse({'status':'object not found'})
    else:
        print("menu_item_update_mini_view is not supported for Get")







class BillListView(ListView):
    paginate_by = 10
    queryset = BillId.objects.all()


def bill_detail_view(request,pk):
    template_name = 'food/billid.html'
    orderlist = Order.get_bill(pk)
# table no is already included in orderlist but template need it outside list (for loop)
    table = orderlist[0]['t']
    return render(request,template_name,{'object_list':orderlist,'id':pk, 'table':table})



#--------------------------order views ----------------------

class OrderListView(LoginRequiredMixin,ListView):
    queryset = Order.objects.all()
    paginate_by = 20


class OrderPendingListView(LoginRequiredMixin,ListView):
    queryset = Order.objects.filter(paid=False)
    template_name = "food/order_list_pending.html"
    paginate_by = 20

import os
from django.shortcuts import redirect
@csrf_exempt
@login_required
def bill_payment_view(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        data_to_print=[]
        try:
            orderlist = Order.objects.filter(table=pk,paid=False)
        except Order.DoesNotExist as e:
            print('not exist')
            return JsonResponse({'status':404,'data':'does not exist'})
        #if bill.paid == True:
        #    print('already paid')

        billid = BillId.objects.create()
        for obj in orderlist:
            obj.paid = True
            obj.billid = billid
            x=obj.save()
            data_to_print.append([obj.item.name,obj.item.price,obj.quantity])
        data_to_print=str(data_to_print)+"@"+str(billid.id)+":"+str(pk)
        os.system(os.getcwd()+"\\print_bill\\print_bill\\bin\\Debug\\print_bill.exe "+data_to_print)
        print('success pay')
        return JsonResponse({'status':'200','id':pk,'data':'bill payment success'})




class OrderDayView(LoginRequiredMixin,DayArchiveView):
    make_object_list = True
    allow_future = True
    queryset = Order.objects.all()
    paginate_by = 20
    date_field = "date"



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import AccountForm
from django.db import IntegrityError
class AccountCreateView(LoginRequiredMixin,View):
    """ account create view in which use contrib.user model """
    form_class = AccountForm
    def get(self,request):
        f = self.form_class()
        return render(request,'registration/accountcreate.html',{'form':f})
    def post(self,request):
        form = self.form_class(request.POST)
        f = self.form_class()
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                x = User(username=form.cleaned_data['username'])
                x.set_password(form.cleaned_data['password1'])
                try:
                    x.save()
                except IntegrityError as e:
                    return render(request,'registration/account.html',{'form':f,'x':'user name is already existed'})
                return redirect('/accountlist/')
        else:
            print(form.error_messages)
        return render(request,'registration/account.html',{'form':f,'x':'form is NUTTT saaved'})


class AccountListView(LoginRequiredMixin,View):
    """ get staff list """
    def get(self,request):
        data = User.objects.filter(is_superuser=False)
        template_name = "registration/accountlist.html"
        return render(request,template_name,{'object_list':data})

@csrf_exempt
@login_required
def delete_account_view(request):
    """ ajax delete user staff """
    user = request.POST['userid']
    try:
        user = User.objects.get(pk= user)
        user.delete()
    except User.DoesNotExist:
        return JsonResponse({'status':'fail'})

    return JsonResponse({'status':'success'})


