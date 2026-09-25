from django.shortcuts import render
from .forms import NameForm
from .forms import SearchForm
from .models import Product

# Create your views here.
def about(request):
    form = SearchForm(request.POST or None)
    products = Product.objects.all()
    if request.method == "POST" and form.is_valid():

        name = form.cleaned_data["name"]
        if name:
            products = Product.objects.filter(name__icontains=name)
            

        
    else:
        products = Product.objects.all()

    return render(request, "about/about.html", {"cars" : products, "form" : form})

def form_view(request):

    if request.method == "POST":
        form = NameForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            category = form.cleaned_data["category"]
            price = form.cleaned_data["price"]

            Product.objects.create(
                name = name,
                category = category,
                price = price
            )
            print(name)
    else:
        form = NameForm()
            
    return render(request, "about/form.html", {"form": form})