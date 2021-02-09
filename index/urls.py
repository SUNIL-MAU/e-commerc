from django.urls import path
from . import views

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('cart/', views.cart.as_view(), name='cart'),
    path('check-out/', views.CheckOut.as_view(), name='checkout'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('search/', views.Search, name='search'),
    path('prod_disc/<int:id>/', views.Product_disc, name='prod_disc'),
    
    
]