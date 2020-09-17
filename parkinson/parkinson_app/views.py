from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model, get_user, logout
from django.core.validators import validate_email, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .backend import CustomBackend
from django.db.models import Q
from django.contrib.auth.models import Permission, Group
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.timesince import timesince
from .ml_model import predict_class
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64, re
from .models import Topic, FAQ, Test

User = get_user_model()

# =================================>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<=======================#
# Create your views here.
def landing_page(request):
    return render(request, 'parkinson_app/landing_page.html')


# ==================================>>>> NEW LOGIN VIEW
def login_page(request):
    if request.method == "POST":
        # Authenticate user
        email=request.POST["email"]
        # password=request.POST["password"]
        password = request.POST.get("password")

        user_email = CustomBackend().authenticate_with_email(request=request, email=email, password=password)
        if user_email is not None:
            login(request, user_email)

            user = get_user(request)
            if user.age == None or user.weight == None or user.height == None:
                return HttpResponseRedirect(reverse('parkinson_app:complete_profile'))

            return HttpResponseRedirect(reverse('parkinson_app:home'))
        else:
            messages.error(request, 'Email or Password error', extra_tags="email_pass_error")
            return HttpResponseRedirect(reverse('parkinson_app:login'))
    else:
        return render(request, 'parkinson_app/login.html')

# -----------------------/////////////////////////////////////////-----------------------------------------------------------------------
# =====================================>>> ENDING NEW LOGIN VIEW <<<=============================
# -----------------------/////////////////////////////////////////----------------------------------------------------------------------

#  =====================================>>> SIGNUP VIEW

def signup_page(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        gender = request.POST["gender-option"]
        password = request.POST["password"]
        try:
            validate_email(email)
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken', extra_tags='email_error')
                return HttpResponseRedirect(reverse('parkinson_app:signup'))
            else:
                user = User.objects.create_user(email=email, password=password, full_name=full_name, gender=gender, phone_number=phone_number,is_staff=None)
                user.save()
                return HttpResponseRedirect(reverse('parkinson_app:login'))

        except ValidationError:
            messages.error(request, 'Email is not a valid email address', extra_tags='email_error')
            return HttpResponseRedirect(reverse('parkinson_app:signup'))
    else:
        return render(request, 'parkinson_app/signup.html')

# =====================================>>> ENDING SIGNUP VIEW

@login_required(login_url='/login')
def home_page(request):
    user = get_user(request)
    try:
        test_result = Test.objects.get(user_id=user.id)
    except:
        test_result = None

    return render(request, 'parkinson_app/home.html',{
        "test_result": test_result
    })

def help_page(request):
    return render(request, 'parkinson_app/help.html')

def faq_page(request):
    topics = Topic.objects.all()
    return render(request, 'parkinson_app/faq_page.html',{
        "topics" : topics,
    })

@login_required(login_url='/login')
def new_test_page(request):
    if request.method == "POST":
        parameters = []
        parameters.append(request.POST["jitter_per"])
        parameters.append(request.POST["jitter_abs"])
        parameters.append(request.POST["jitter_ddp"])
        parameters.append(request.POST["mdvp_ppq"])
        parameters.append(request.POST["mdvp_rap"])
        parameters.append(request.POST["mdvp_shimmer"])
        parameters.append(request.POST["mdvp_shimmer_db"])
        parameters.append(request.POST["shimmer_apq3"])
        parameters.append(request.POST["shimmer_apq5"])
        parameters.append(request.POST["mvp_avq"])
        parameters.append(request.POST["shimmer_dda"])
        parameters.append(request.POST["rpde"])
        parameters.append(request.POST["d2"])
        parameters.append(request.POST["nhr"])
        parameters.append(request.POST["spread2"])
        parameters.append(request.POST["ppe"])

        for parameter in parameters:
            if parameter == None or parameter == "":
                print("Please fill all fields")
                messages.error(request, "Please Fill all fields", extra_tags="field_error")
                return HttpResponseRedirect(reverse('parkinson_app:new_test'))

        jitter_per = float(request.POST["jitter_per"])
        jitter_abs = float(request.POST["jitter_abs"])
        jitter_ddp = float(request.POST["jitter_ddp"])
        mdvp_ppq = float(request.POST["mdvp_ppq"])
        mdvp_rap = float(request.POST["mdvp_rap"])
        mdvp_shimmer = float(request.POST["mdvp_shimmer"])
        mdvp_shimmer_db = float(request.POST["mdvp_shimmer_db"])
        shimmer_apq3 = float(request.POST["shimmer_apq3"])
        shimmer_apq5 = float(request.POST["shimmer_apq5"])
        mvp_avq = float(request.POST["mvp_avq"])
        shimmer_dda = float(request.POST["shimmer_dda"])
        rpde = float(request.POST["rpde"])
        d2 = float(request.POST["d2"])
        nhr = float(request.POST["nhr"])
        spread2 = float(request.POST["spread2"])
        ppe = float(request.POST["ppe"])

        result = predict_class(jitter_per, jitter_abs, jitter_ddp, mdvp_ppq, mdvp_rap, mdvp_shimmer, mdvp_shimmer_db, shimmer_apq3, shimmer_apq5, mvp_avq, shimmer_dda, rpde, d2, nhr, spread2, ppe)
        # status 1 = sick, 0 = healthy
        final_pred = " "

        if result == 1:
            final_pred = "Sick Patient"
        else:
            final_pred = "Healthy Patient"
        user = get_user(request)

        try:
            Test.objects.filter(user_id=user.id).delete()
        except:
            pass

        test_data = Test(user_id=user.id, Jitter_percentage=jitter_per, Jitter_absolute=jitter_abs, Jitter_ddp=jitter_ddp, mdvp_ppq=mdvp_ppq, mdvp_rap=mdvp_rap, mdvp_shimmer=mdvp_shimmer, mdvp_shimmer_db=mdvp_shimmer_db, shimmer_apq3=shimmer_apq3, shimmer_apq5=shimmer_apq5, mdvp_avq=mvp_avq, shimmer_dda=shimmer_dda, rpde=rpde, d2=d2, nhr=nhr, spread_2=spread2, ppe=ppe, result=result)
        test_data.save()

        print(final_pred)
        return render(request, 'parkinson_app/new_test.html', {
            "final_pred": final_pred
        })

    return render(request, 'parkinson_app/new_test.html')


@login_required(login_url='/login')
def edit_profile_page(request):
    if request.method == "POST":
        name = request.POST["full_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        gender = request.POST["gender"]
        age = request.POST["age"]
        weight = request.POST["weight"]
        height = request.POST["height"]

        if (age == None or age == "") and (weight == None or weight == "") and (height == None or height == "") and (name == None or name == "") and (email == None or email == "") and (phone_number == None or phone_number == "") and (gender == None or gender == ""):
            return render(request, "parkinson_app/edit_profile.html", {
                "error": "Please provide all required information!"
            })

        user = get_user(request)
        user.full_name = name
        user.email = email
        user.phone_number = phone_number
        user.gender = gender
        user.age = age
        user.weight = weight
        user.height = height
        user.save()

        return HttpResponseRedirect(reverse('parkinson_app:edit_profile'), {
            "success" : "Profile Information Updated",
        })

    return render(request, 'parkinson_app/edit_profile.html')

def what_is_parkinson_page(request):
    return render(request, 'parkinson_app/what_is_parkinson.html')

# ===================================== LOGOUT SECTION
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('parkinson_app:login'))


@login_required(login_url='/login')
@csrf_exempt
def upload_profile_pic(request):
    print(request.POST.get("image"))
    if request.POST.get("image"):
        user = get_user(request)
        user = User.objects.get(id=user.id)
        image_file = request.POST['image']
        imgformat, imgstr = image_file.split(';base64,') 
        ext = imgformat.split('/')[-1] 

        data = ContentFile(base64.b64decode(imgstr), name=user.full_name+'-'+str(datetime.now)+'.' + ext)
        fs = FileSystemStorage()
        file_name = fs.save(user.full_name, data)
        # uploaded_url = fs.url(file_name)
        user.profile_img = file_name
        user.save()

        return HttpResponseRedirect(reverse('parkinson_app:home'))

    return HttpResponseRedirect(reverse('parkinson_app:home'))


@login_required(login_url='/login')
def update_password(request):
    password = request.POST["password"]
    conf_password = request.POST["confirm_password"]

    if password == None or password == "":
        return render(request, 'parkinson_app/edit_profile.html',{
            "error":"Please Fillup password fields!"
        })

    if password == conf_password:
        user = get_user(request)
        user.set_password(password)
        user.save()
        return render(request, 'parkinson_app/edit_profile.html',{
            "success":"Password Updated!"
        })        
    
    return render(request, 'parkinson_app/edit_profile.html',{
        "error":"Password didn't matched!"
    })


@login_required(login_url="/login")
def complete_profile(request):
    if request.method == "POST":
        age = request.POST["age"]
        weight = request.POST["weight"]
        height = request.POST["height"]

        if (age == None or age == "") and (weight == None or weight == "") and (height == None or height == ""):
            return render(request, "parkinson_app/complete_profile.html", {
                "error": "Please provide all required information!"
            })
    
        user = get_user(request)
        user.age = age
        user.weight = weight
        user.height = height
        user.save()

        return HttpResponseRedirect(reverse("parkinson_app:home"))


    return render(request, 'parkinson_app/complete_profile.html')