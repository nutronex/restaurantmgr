from django.db import models
from django.db.models import  Sum
from django.core.urlresolvers import  reverse

class Fuck(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    def __str__(self):
        return self.name + " " + str(self.age)

# Create your models here.
food_type = [('veg','vegetarian'),
             ('sea','seafood'),
             ('pork','pork'),
             ('chicken','chicken')]

class FoodCategory(models.Model):
    name = models.CharField(max_length= 20)

    def get_absolute_url(self):
        return reverse('home')
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200,blank=True)
    #changed from meat to category m2m realtion ; shrimp salad  can be salad and seafood
    category = models.ManyToManyField(FoodCategory,related_name='menuitem')
    price = models.IntegerField()
    image = models.ImageField(upload_to='myimgfolder/',blank=True)
    favourite = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('-name',)
    def get_absolute_url(self):
        return reverse('home')


class BillId(models.Model):
#    paid = models.BooleanField(default=False)
    def __str__(self):
        return str(self.pk)

class Order(models.Model):

    billid = models.ForeignKey(BillId,null=True)
    item = models.ForeignKey(MenuItem)
    quantity = models.IntegerField()
    table = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField(default = False)
    parcle = models.BooleanField(default = False)
    paid = models.BooleanField(default=False)


    @staticmethod
    def get_bill(table=None,xid=None):
        """return bill dictionary from bill id
           coz customer may order same item several times"""
        """
        **** supplyment  ***
        omitted xid voucher id and use table id and paid=false
        """

        if table ==None:
            return None
        try:
          #  orderlist =  Order.objects.filter(billid_id=xid,paid=False)
            orderlist =  Order.objects.filter(table=table,paid=False)

            table = orderlist[0].table
        except Order.DoesNotExist:
            return None
        if not orderlist :
            return {}
        itemlist = set(x.item.name for x in orderlist )
        if not itemlist:
            return {}
        data = {}
        data = []
        try:
            for i in itemlist:
                order = orderlist.filter(item__name=i)
                qty = order.aggregate(Sum('quantity'))
                qty ={'n':i,'q': qty['quantity__sum'],'p':order[0].item.price ,'t':orderlist[0].table}
                data.append(qty)
        except IndexError as e:
            return {}

        return data



    def __str__(self):
        return "item : {0}  |qty : {1}  | table  : {2}".format(self.item, self.quantity,self.table)


class A(models.Model):
    name = models.CharField(max_length= 20)
class B(models.Model):
    name = models.CharField(max_length =20)
    alink = models.ForeignKey(A,null=True,blank=True)
