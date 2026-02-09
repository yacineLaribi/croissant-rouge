from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser , Distribution
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db import models
from django.contrib import messages
from django.db import IntegrityError


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
        
            # Validate required fields
            fullname = request.POST.get("fullname")
            aid_type = request.POST.get("aidType")
            date = request.POST.get("date")
            
            if not fullname or not aid_type:
                messages.error(request, "Veuillez remplir tous les champs obligatoires.")
                return render(request, "save-beneficiary.html")
            
            # Check if at least one ID is provided
            nin = request.POST.get("idNumber") or None
            ccp = request.POST.get("passport") or None
            
            if not nin and not ccp:
                messages.error(request, "Veuillez fournir soit le NIN soit le numéro de CCP.")
                return render(request, "save-beneficiary.html")
            
            # Create distribution record
            Distribution.objects.create(
                fullname=fullname,
                address=request.POST.get("adress"),
                commune=request.POST.get("commune"),
                nin=nin,
                ccp_or_passport=ccp,
                aid_type=aid_type,
                distribution_date=date or now().date(),
                notes=request.POST.get("notes"),
                created_by=request.user,
            )
            
            messages.success(request, "Distribution enregistrée avec succès!")
            return redirect("save")
            
        # except IntegrityError:
        #     messages.error(request, "Erreur: Cette entrée existe déjà dans le système.")
        #     return render(request, "save-beneficiary.html")
        
        # except Exception as e:
        #     messages.error(request, f"Une erreur s'est produite: {str(e)}")
        #     return render(request, "save-beneficiary.html")

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
