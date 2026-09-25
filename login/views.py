from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
def login_view(request):
    print("METHOD:", request.method)
    print("POST:", request.POST)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return render(request, "login/login.html")
    return render(request, "login/login.html")