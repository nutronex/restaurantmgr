#here in test file completed test functions are prefixed by 'x' eg xtest_order_get()


from django.test import TestCase

# Create your tests here.
from .models import  *
from .serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO
from django.contrib.auth.models import User
import json
import requests as req


class TestModelAggregate(TestCase):
    def setUp(self):
        passwd = 'asdfghjkl'
        ''' create user for authentication'''
        x = User.objects.create(username='ak',email='fo@ak.ak')
        x.set_password(passwd)
        x.save()
        #x=self.client.login(username='ak' ,password=passwd)
        print(x)
        BillId.objects.create(pk=45)
        BillId.objects.create(pk=538)
        x = MenuItem(name='kyae Oh',price=3500)
        y = MenuItem(name='Myanmar Beer',price=1500)
        x.save()
        y.save()

        x.category.add(FoodCategory.objects.create(name="pork"))
        y.category.add(FoodCategory.objects.create(name="drink"))
        y.category.add(FoodCategory.objects.create(name="liquor"))

        order_list = [{"item":1,"table":345,"billid":45,"quantity":8},
                      {"item":2,"table":345,"billid":538,"quantity":3},
                      {"item":2,"table":345 ,"quantity":233}]

        for x in order_list:
            o = OrderSerializer(data=x)
            if o.is_valid() :
        #        o.save()
                pass
            else :
                print(o.errors)



    def xtest_OrderSerializer_add_multi_item_and_retrive_bill(self):
        print(Order.get_bill(45))
        pass

    def xtest_order_get(self):
        x = self.client.get('/api/order/',content_type='application/json')
        print(x.content)
        print("------------")


    def xtest_order_post_delete_put(self):
        data = {"item":2,"table":345 ,"quantity":11111}
        data = json.dumps(data)
        x = self.client.post('/api/orderadd/',data,content_type='application/json')
        print("start request")
        self.xtest_order_get()

        x=self.client.delete('/api/orderadd/1/')
        print("delete request")
        self.xtest_order_get()

        data = {"item":1,"table":345 ,"quantity":9999}
        data = json.dumps(data)
        x = self.client.post('/api/orderadd/',data,content_type='application/json')
        print("post request")
        self.xtest_order_get()

        data = {"item":2,"table":345 ,"quantity":888888}
        data = json.dumps(data)
        x = self.client.put('/api/orderadd/2/',data,content_type='application/json')
        print(x.status_code)
        print("put request")
        self.xtest_order_get()

    def test_userlogin_plain_http(self):
        x =self.client.get('/api/order/',content_type='application/json')
        print(x)


