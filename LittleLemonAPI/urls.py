from django.urls import path
from. import views

urlpatterns = [
    path("menu-items/",views.MeniView.as_view()),
    path("menu-items/<int:pk>",views.MenuiViewitem.as_view()),
    path("groups/manager/users/",views.ManagerView.as_view()),
    path("groups/delivery-crew/users/",views.DeliveryView.as_view()),
    path("cart/menuitem/",views.CartView.as_view()),
    path("orders/",views.CartItemView.as_view()),
    path("orders/<int:pk>",views.OrderView.as_view())

]

