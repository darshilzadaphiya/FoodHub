from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from rest_framework.decorators import api_view

from .models import Item
from .forms import ItemForm
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import logging
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

@api_view(['GET'])
def item_list_api(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

def item_list_json(request):
    items = Item.objects.all().values("id", "item_name", "item_price")
    return JsonResponse(list(items), safe=False)
# Create your views here.
# @login_required()
# @cache_page(60 * 15)
# @vary_on_headers("User-Agent")
def index(request):
    # Getting items from the database
    logger.info("Fetching all items from the database")
    logger.info(f"User [{timezone.now().isoformat()}] {request.user} requested item list from {request.META.get('REMOTE_ADDR')}")
    item_list = Item.objects.all()
    logger.debug(f"Found {item_list.count()} items in the database")
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

def detail(request, id):
    # Getting single item as per id
    logger.info(f"Fetching item with id {id}")
    try:
        item = get_object_or_404(Item, pk=id)
        logger.debug(f"Found {item.item_name} (${item.item_price})")
    except Exception as e:
        logger.error("Error fetching the item %s:  %s", id,e)
        raise
    return render(request, "myapp/detail.html", {"item":item})

# class FoodDetail(DetailView):
#     model = Item
#     template_name = "myapp/detail.html"
#     context_object_name = 'item'


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