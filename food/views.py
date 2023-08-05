from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item
from django.template import loader
from .forms import ItemForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView
# Create your views here.
def index(request):
    item_list = Item.objects.all()
    # template = loader.get_template('food/index.html')
    context = {
        'item_list' : item_list,
    }
    # return HttpResponse(template.render(context,request))
    return render (request,'food/index.html',context)

# this works same as above index function only difference is that it is class based inbuilt view
class IndexClassView(ListView):
    model = Item;
    template_name = 'food/index.html'
    context_object_name = 'item_list'



def item(request):
    return HttpResponse('<h1>this is an item view</h1>')

# def detail(request,item_id):
#     return HttpResponse ("This is item no/id: %s"%item_id)
def detail(request,item_id):
    item = Item.objects.get(pk=item_id)
    context = {
        'item':item,
    }
    return render(request,'food/detail.html',context)

class FoodDetail(DetailView):
    model = Item
    template_name = 'food/detail.html'



def create_item(request):
    form = ItemForm(request.POST or None)
    context = {
        'form':form,
    }
    if form.is_valid():
        form.save()
        return redirect('food:index')
    return render (request,'food/item-form.html',context)

# this is class view of create_item
class CreateItem(CreateView):
    model = Item
    fields = ['item_name','item_desc','item_price','item_image']
    template_name = 'food/item-form.html'

    def form_valid(self,form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

def update_item(request,id):
    item = Item.objects.get(pk=id)
    form = ItemForm(request.POST or None,instance=item)
    context = {
        'item':item,
        'form':form,
    }
    if form.is_valid():
        form.save()
        return redirect ('food:index')
    return render (request,'food/item-form.html',context)

def delete_item(request,id):
    item = Item.objects.get(id=id)
    # context = {
    #     'item':item,
    # }
    if request.method=="POST":
        item.delete()
        return redirect ('food:index')
    return render (request,'food/item-delete.html',{'item':item})