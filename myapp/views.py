from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from .models import Item
from .forms import ItemForm
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

# Create your views here.
@login_required()
# @cache_page(60 * 15)
def index(request):
    # Getting items from the database
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Creating Context
    context = {'page_obj':page_obj}
    # return HttpResponse(item_list)
    return render(request, "myapp/index.html", context)

# This is a class based view
# class IndexClassView(ListView):
#     model = Item
#     template_name = "myapp/index.html"
#     context_object_name = 'item_list'

# def detail(request, id):
#     # Getting single item as per id
#     item = Item.objects.get(id=id)
#     return render(request, "myapp/detail.html", {"item":item})
    # return HttpResponse(f"This is the detail view for item with id as {id} and details are {item_detail}")

class FoodDetail(DetailView):
    model = Item
    template_name = "myapp/detail.html"
    context_object_name = 'item'


@login_required()
def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method=="POST":
        form = ItemForm(request.POST)
        form.instance.user_name = request.user
        if form.is_valid():
            form.save()
            return redirect("myapp:index")
    return render(request, "myapp/item-form.html", {"form":form})

# class ItemCreateView(CreateView):
#     model = Item
#     fields = ['item_name', 'item_desc', 'item_price', 'item_image' ]
#     # form_class = ItemForm


def update_Item(request, id):
    item = Item.objects.get(id=id)
    if item.user_name != request.user:
        return redirect("myapp:index")
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect("myapp:index")
    return render(request, "myapp/item-form.html", {"form":form})

def delete_Item(request, id):
    item = Item.objects.get(id=id)
    if request.method=="POST":
        item.delete()
        return redirect("myapp:index")
    return render(request, "myapp/item-delete.html")

def get_objects_optimized(request):
    items = Item.objects.only('item_name')
    for item in items:
        print(item.item_name)