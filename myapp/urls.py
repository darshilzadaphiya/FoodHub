from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
app_name = 'myapp'

urlpatterns = [
    # URL Patterns of API
    # path('item-json/',views.item_list_json,name='item_list_json'),
    # URL Patterns of API built with REST
    path('item-json/',views.item_list_api,name='item_list_api'),

    # URL Patterns of Django App
    # path('',views.index, name='index'),
    # path('',cache_page(60*15)(views.index), name='index'),
    path('',views.index, name='index'),
    path('<int:id>/',views.detail, name='detail'),
    # path('<int:pk>/',views.FoodDetail.as_view(), name='detail'),
    # path('add/', views.create_item, name='create_item'),
    path('add/', views.create_item, name='create_item'),
    path('update/<int:id>/', views.update_Item, name='update_item'),
    path('delete/<int:id>/', views.delete_Item, name='delete_item'),
]