from django.urls import path,re_path
from . import views

app_name='shop'
urlpatterns = [
    path('', views.index, name ="ShopHome" ),
    path('about/', views.about, name ="Aboutus" ),
    path('contact/', views.contact, name ="Contactus" ),
    path('search/', views.search, name ="Search" ),
    path('tracker/', views.tracker, name ="Trackingstatus" ),
    path('checkout/', views.checkout, name ="Checkout" ),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/',views.index, name='home'),
    path('pay/',views.djangopayment,name ='pay'),
    re_path('pays/success', views.success, name='success'),
    re_path('pays/declined', views.declined, name='declined'),

]