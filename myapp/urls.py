from django.urls import path
from . import views
app_name = 'myapp'

urlpatterns = [
    path('',views.index, name='index'),
    # path('<int:id>/',views.detail, name='detail'),
    path('<int:pk>/',views.FoodDetail.as_view(), name='detail'),
    # path('add/', views.create_item, name='create_item'),
    path('add/', views.create_item, name='create_item'),
    path('update/<int:id>/', views.update_Item, name='update_item'),
    path('delete/<int:id>/', views.delete_Item, name='delete_item'),
]