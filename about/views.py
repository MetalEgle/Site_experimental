from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from .forms import NameForm
from .forms import SearchForm
from .models import Product


def about(request):
    search_form = SearchForm(request.GET or None)
    product_list = Product.objects.all()

    if search_form.is_valid():
        search_query = search_form.cleaned_data["name"]
        selected_body_types = search_form.cleaned_data["body_types"]

        if search_query:
            product_list = product_list.filter(
                Q(name__icontains=search_query)
                | Q(category__icontains=search_query)
            )
        if selected_body_types:
            product_list = product_list.filter(body__in=selected_body_types)

    return render(
        request,
        "about/about.html",
        {"products": product_list, "form": search_form},
    )


def form_view(request):
    if request.method == "POST":
        form = NameForm(request.POST)

        if form.is_valid():
            product_name = form.cleaned_data["name"]
            product_category = form.cleaned_data["category"]
            product_price = form.cleaned_data["price"]
            product_body = form.cleaned_data["body"]

            # Создаём запись только после успешной проверки всех полей формы.
            Product.objects.create(
                name=product_name,
                category=product_category,
                price=product_price,
                body=product_body,
            )
            messages.success(request, "Автомобиль успешно добавлен!")
            return redirect("add_product")
    else:
        form = NameForm()

    return render(request, "about/form.html", {"form": form})