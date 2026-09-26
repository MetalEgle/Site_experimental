from django.contrib import messages
from django.core.paginator import Paginator
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

    paginator = Paginator(product_list.order_by("pk"), 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    next_page_query = None
    if page_obj.has_next():
        query_params = request.GET.copy()
        query_params["page"] = page_obj.next_page_number()
        next_page_query = query_params.urlencode()

    return render(
        request,
        "about/about.html",
        {
            "products": page_obj.object_list,
            "page_obj": page_obj,
            "next_page_query": next_page_query,
            "form": search_form,
        },
    )


def form_view(request):
    if request.method == "POST":
        form = NameForm(request.POST, request.FILES)

        if form.is_valid():
            product_name = form.cleaned_data["name"]
            product_category = form.cleaned_data["category"]
            product_price = form.cleaned_data["price"]
            product_body = form.cleaned_data["body"]
            product_image = form.cleaned_data["image"]

            # Создаём запись только после успешной проверки всех полей формы.
            Product.objects.create(
                name=product_name,
                category=product_category,
                price=product_price,
                body=product_body,
                image=product_image,
            )
            messages.success(request, "Автомобиль успешно добавлен!")
            return redirect("add_product")
    else:
        form = NameForm()

    return render(request, "about/form.html", {"form": form})