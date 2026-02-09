from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser , Distribution
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db import models


# Create your views here.
@login_required
def home(request):
    context = {}

    if request.method == "POST":
        identifier = request.POST.get("identifier")

        distribution = Distribution.objects.filter(
            models.Q(nin=identifier) |
            models.Q(ccp_or_passport=identifier)
        ).order_by("-distribution_date").first()

        if distribution:
            context["status"] = "received"
            context["distribution"] = distribution
        else:
            context["status"] = "eligible"
            context["identifier"] = identifier

    return render(request, "home.html", context)

@login_required
def save_beneficiary(request):
    if request.method == "POST":
        Distribution.objects.create(
            fullname=request.POST.get("fullname"),
            address=request.POST.get("adress"),
            commune=request.POST.get("commune"),
            nin=request.POST.get("idNumber") or None,
            ccp_or_passport=request.POST.get("passport") or None,
            aid_type=request.POST.get("aidType"),
            distribution_date=request.POST.get("date") or now().date(),
            notes=request.POST.get("notes"),
        )
        return redirect("save")  # or any success page

    return render(request, "save-beneficiary.html")

@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
def dashboard(request):
    return render(request,'dashboard.html')




def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        fullname = request.POST.get('fullname')
        organisation = request.POST.get('organisation')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            fullname=fullname,
            organisation=organisation,
            username=email
        )

        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid email or password')
        return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
