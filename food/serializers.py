from .models import FoodCategory , MenuItem ,Order ,BillId
from rest_framework.serializers import  HyperlinkedModelSerializer
from rest_framework import serializers
from .models import Fuck
class Fuckx(serializers.ModelSerializer):
    class Meta:
        model = Fuck
        fields =('name','age')


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields =('name','id')


class MenuItemSerializer(serializers.ModelSerializer):

#    category = serializers.StringRelatedField(many = True,read_only = True)

    class Meta:
        model = MenuItem
        fields = ('id','name','description','price','category','image')


class OrderSerializer(serializers.ModelSerializer):

    def create(self,kwarg):
        """ for new order without billid create new billid  """

        item_name =kwarg.get('item',None)

#        if not 'billid' in kwarg:
#            a = BillId.objects.create()
#            kwarg.update({'billid':a})
        return super().create(kwarg)

    def update(self,i,s):
        print("xxx")
        return 34 #pass

    class Meta:
        model = Order
        fields = ('pk','billid','item','quantity','table','date','parcle',)



class OrderSerializerVerbose(OrderSerializer):
    """  override item id from parent to string """
    item = serializers.StringRelatedField()



