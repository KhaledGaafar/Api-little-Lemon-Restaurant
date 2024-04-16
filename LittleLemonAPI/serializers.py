from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal
from .models import MenuItem, Category ,Cart,OrderItem,Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email",'id'] 

class CategorySerializer (serializers.ModelSerializer):

    class Meta:
         model = Category
         fields = ['id','slug','title']
         
class MenuItemSerializer(serializers.ModelSerializer):

    
    #category = CategorySerializer(read_only=True)
    category_id=serializers.IntegerField()
    
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured',"category_id"]
class CartSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    menuitem=MenuItemSerializer(read_only=True)
    menuitem_id=serializers.IntegerField(write_only=True)
    price=serializers.SerializerMethodField(method_name="count_price",read_only=True)

    class Meta:
        model=Cart
        fields=["user","menuitem",'quantity',"unit_price","price","menuitem_id"]
    def count_price(self,pro:Cart):
        return pro.unit_price * pro.quantity
    
    
    

class OrderItemSerializer(serializers.ModelSerializer):


    class Meta:
        model=OrderItem
        fields=["order","menuitem","quantity","unit_price","price"]

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        fields=["user","delivery_crew","status","total","date"]


    
    
  
        