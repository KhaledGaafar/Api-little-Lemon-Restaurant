from django.shortcuts import render,get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .models import MenuItem,Category,Cart,OrderItem,Order
from .serializers import MenuItemSerializer,CartSerializer,OrderItemSerializer,OrderSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User,Group
from rest_framework.views import APIView
from .serializers import UserSerializer 
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle




class MeniView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    ordering_fields=['price']
    search_fields=['title']
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):

       if self.request.user.groups.filter( name="Manager").exists():
            return  super().create(request, *args, **kwargs) 
       else:
             return Response ({"message":"you are not authorized"},status.HTTP_401_UNAUTHORIZED)
       

class MenuiViewitem(generics.RetrieveUpdateDestroyAPIView):
     queryset=MenuItem.objects.all()
     serializer_class=MenuItemSerializer
     permission_classes=[IsAuthenticated]

     def update(self, request, *args, **kwargs):
          if self.request.user.groups.filter( name="Manager").exists():
            return  super().update(request, *args, **kwargs) 
          else:
             return Response ({"message":"you are not authorized"},status.HTTP_401_UNAUTHORIZED)
        
     def destroy(self, request, *args, **kwargs):
         if self.request.user.groups.filter( name="Manager").exists():
            return  super().destroy(request, *args, **kwargs) 
         else:
             return Response ({"message":"you are not authorized"},status.HTTP_401_UNAUTHORIZED)  
      

class ManagerView(APIView):
    
    def get(self, request):
        if request.user.groups.filter( name="Manager").exists():
          managers = Group.objects.get(name="Manager")
          serializer = UserSerializer(managers.user_set.all(), many=True)
          return Response(serializer.data)
        return Response({"message":"You are not authorize"},status.HTTP_401_UNAUTHORIZED)


    def post(self, request):
        if request.user.groups.filter( name="Manager").exists():
             username = request.data.get("username")
             if username:
                user = get_object_or_404(User, username=username)
                managers = Group.objects.get(name="Manager")
                managers.user_set.add(user)
                return Response({"message": "User added to Manager group"}, status=status.HTTP_201_CREATED)
             return Response({"message": "Invalid input"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"You are not authorize"},status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.groups.filter( name="Manager").exists():
            username = request.data.get("username")
            if username:
                user = get_object_or_404(User, username=username)
                managers = Group.objects.get(name="Manager")
                managers.user_set.remove(user)
                return Response({"message": "User removed from Manager group"}, status=status.HTTP_202_ACCEPTED)
            return Response({"message": "Invalid input"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"You are not authorize"},status.HTTP_401_UNAUTHORIZED)
    

class DeliveryView(APIView):
    
    def get(self, request):
        if request.user.groups.filter( name="Manager").exists():
          Delivery = Group.objects.get(name="Delivery crew")
          serializer = UserSerializer(Delivery.user_set.all(), many=True)
          return Response(serializer.data)
        return Response({"message":"You are not authorize"},status.HTTP_401_UNAUTHORIZED)


    def post(self, request):
        if request.user.groups.filter( name="Manager").exists():
             username = request.data.get("username")
             if username:
                user = get_object_or_404(User, username=username)
                Delivery = Group.objects.get(name="Delivery crew")
                Delivery.user_set.add(user)
                return Response({"message": "User added to Delivery group"}, status=status.HTTP_201_CREATED)
             return Response({"message": "Invalid input"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"You are not authorize"},status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.groups.filter( name="Manager").exists():
            username = request.data.get("username")
            if username:
                user = get_object_or_404(User, username=username)
                Delivery = Group.objects.get(name="Delivery crew")
                Delivery.user_set.remove(user)
                return Response({"message": "User removed from Delivery group"}, status=status.HTTP_202_ACCEPTED)
            return Response({"message": "Invalid input"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"You are not authorize"},status.HTTP_401_UNAUTHORIZED)

class CartView(generics.ListCreateAPIView,generics.DestroyAPIView):
    
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]


    def create(self, request, *args, **kwargs):
        id=self.request.data.get("menuitem_id")
        items=MenuItem.objects.filter(id=id)

        
        for item in items:
            cart=Cart.objects.create(
            unit_price=item.price,
            quantity=self.request.data.get("quantity"),
            user_id=self.request.user.id ,
            menuitem_id=self.request.data.get("menuitem_id"), 
                   
            )
        cart.save()
    
        return Response({"message":"created"},status.HTTP_201_CREATED)
        

    def list(self, request, *args, **kwargs):
        
        user_id=request.user.id
    
        user_info=Cart.objects.get(user_id=user_id)
        serializer=CartSerializer(user_info)
        return Response(serializer.data)
        
    def destroy(self, request, *args, **kwargs):
        user_id=request.user.id
        user_info=Cart.objects.get(user_id=user_id)
        user_info.user = request.user
        user_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    permission_classes=[IsAuthenticated]
    ordering_fields=['quantity']
    search_fields=['title']
    
    def list(self, request, *args, **kwargs):
         
         if self.request.user.groups.filter( name="Manager").exists():
             return super().list(request, *args, **kwargs)
        
         elif self.request.user.groups.filter( name="Delivey crew").exists():
             item= Order.objects.filter(delivery_crew=self.request.user)
             serializer=OrderSerializer(item)
             return Response(serializer.data)

         else:
            user_id=self.request.user.id
    
            user_info=OrderItem.objects.get(order_id=user_id)
            serializer=OrderItemSerializer(user_info)
            return Response(serializer.data)
         
    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user)

        for  cart_item in cart:
            order_item = OrderItem.objects.create(
            menuitem=cart_item.menuitem,    
            order=cart_item.user,
            unit_price=cart_item.unit_price,
            price=cart_item.price,  
            quantity=cart_item.quantity
          )
            order_item.save()
            cart.delete()
         
        return Response(status.HTTP_201_CREATED)
    
       
    
class OrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
   
    def retrieve(self, request, *args, **kwargs):
 
            pk = self.kwargs['pk']
            if pk==self.request.user.id:
              items=OrderItem.objects.get(order_id=pk)
              serializer=OrderItemSerializer(items)
              return Response(serializer.data)
            else:
                return Response({"message":"you are not right person"})
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user.groups.filter( name="Manager").exists():
             
             pk = self.kwargs['pk']
             user_info=Order.objects.get(id=pk)
             user_info.user = request.user
             user_info.delete()
             return Response(status=status.HTTP_204_NO_CONTENT)
        
    def partial_update(self, request, *args, **kwargs):

           if self.request.user.groups.filter( name="Delivey crew").exists():
               instance=Order.objects.get(delivery_crew=self.request.user)
               status=self.request.data.get("status")
               instance.status.add(status)
               instance.save()
               return Response({"message":"status updated"})
           else:
            
             return super().partial_update(request, *args, **kwargs)


    
   
        

    

   
    
   