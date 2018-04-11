from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
from django.http import Http404
from food.models import Order
from datetime import date
from food.serializers import OrderSerializerVerbose
from django.db.models import  Sum
# Create your views here.

def index(request):
    today = date.today()
    qtylist=[]
    daylist=[]
    for i in range(1,31):
        qty=  Order.objects.filter(date__year=today.year,
                                   date__month=today.month,
                                   date__day=i).aggregate(totalqty=Sum('quantity'))["totalqty"]
        if qty:
            daylist.append(i)
            qtylist.append(qty)
    return render(request,"report_index.html",{"days":daylist, "qty":qtylist})




def day_view(request,year,month,day=0):
    rdate = year+" / "+month+" / "+(day if day else "")

    try:
        _year = int(year)
        _month = int(month)
        #if day is "" ,i set it to 0 ,
        _day = int(0 if day =="" else day )
    except ValueError as e :
        pass

    #the request date may be yy/mm/ or yy/mm/dd in later case  date(yy,mm,0) will end up with fucking error
    if _day :
        requested_date = date(_year,_month,_day)
        data = Order.objects.filter(date__contains= requested_date )
    else :
        data = Order.objects.filter(date__year = year , date__month = month )
    itemlist = set(x.item.name for x in data )

    totalp=0
    totalq=0
    data_toreturn = []

    if  itemlist:
        for i in itemlist:
            order = data.filter(item__name=i)
            qty = order.aggregate(Sum('quantity'))
            qty ={'n':i,'q': qty['quantity__sum'],'p':order[0].item.price }
            totalp += (qty['q'] * order[0].item.price)
            totalq += qty['q']
            data_toreturn.append(qty)

    return render(request,"date.html",{"date":rdate,"data":data_toreturn,"q":totalq,"p":totalp})






def api_day_view(request,year,month,day=0):

    try:
        _year = int(year)
        _month = int(month)
        #if day is "" ,i set it to 0 ,
        _day = int(0 if day =="" else day )
    except ValueError as e :
        return JsonResponse({"data":"invalid date format"},status=404)

    #the request date may be yy/mm/ or yy/mm/dd in later case  date(yy,mm,0) will end up with fucking error
    if _day :
        requested_date = date(_year,_month,_day)
        data = Order.objects.filter(date__contains= requested_date )
    else :
        data = Order.objects.filter(date__year = year , date__month = month )

    result = OrderSerializerVerbose(data,many=True)
    return JsonResponse({"data":result.data})





