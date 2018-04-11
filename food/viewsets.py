from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
#,CreateAPIView,DestroyAPIView
from .models import Order,BillId,MenuItem,FoodCategory
from .serializers import OrderSerializerVerbose
from .serializers import OrderSerializer
from .serializers import FoodCategorySerializer
from .serializers import MenuItemSerializer
from .serializers import Fuckx
from django.views.generic import  ListView,DetailView
from .forms import MenuItemForm , FoodCategoryForm
from .permissions import IsStaff
from rest_framework import permissions
from django.http import JsonResponse

import os
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import os
class FuckV(GenericAPIView):
    """
    get list of json data(list of order) ,and save to db coz drf  doesnt support bulk operation

    """
    serializer_class = OrderSerializer

    @method_decorator(login_required)
    def post(self,request):
        #print("in post")
        #print(request.data["items"])
        data = request.data["items"]
        if isinstance(data, list) :
            to_print=[]
            #here remove [x,y,none] from data
            datax = [x for x in data if x is not None]
            for i in datax:
                if int(i["quantity"]) > 0:
                    x = self.serializer_class(data=i)
                    if x.is_valid():
                        c=x.save()
                        printitem = [str(c.item),c.quantity,c.table]
                        #print(x.parcle)
                        if request.data.get("parcle",""):
                            print("this is parcle")
                            printitem[0]+="(p)"
                        to_print.append(printitem)

                    else:
                        return JsonResponse({"data":"fail",})
            to_print=str(to_print)
            print(to_print)
            os.system(os.getcwd()+"\\ConsoleApplication1\\ConsoleApplication1\\bin\\Debug\\ConsoleApplication1.exe"+" "+str(to_print))
            return JsonResponse({"data":"success",})
        print("data is not LIST ")
        return JsonResponse({"data":"error request",})


class OrderVerboseViewSet(ReadOnlyModelViewSet):
    """ views for order list with menuitem name """
   # model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializerVerbose
    http_method_names =['get',]
    lookup_field="date"


from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

class OrderAddViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """ view to add new order without billid ,if  billid is not included in request it will be created in serializer"""

    def get_serializer_wrapper():
        def fn(*a,**ka):
            return OrderSerializer(many=True,*a,**ka)
        return fn

    queryset = Order.objects.all()
    #serializer_class =get_serializer_wrapper()
    serializer_class = OrderSerializer
    http_method_names =['get','post','delete',]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

class BillViewSet(ModelViewSet):
    queryset = BillId.objects.all()
    http_method_names =['get',]

class FoodCategoryViewSet(ModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    http_method_names =['get',]

class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    http_method_names = ['get',]
