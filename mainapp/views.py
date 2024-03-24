from ast import Return
from email.message import Message
from itertools import count
from turtle import update
from unicodedata import category
# from ssl import _PasswordType
from django.db.models import Avg,Max,Min,Sum,Count,StdDev,Variance
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from adminapp.models import *
from mainapp.models import *
from userapp.models import *
import pytesseract
import PIL.Image
# import imutils
import cv2
import os


# Create your views here.


def home_index(request):
    return render(request,"home/home-index.html")


def home_admin_login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        

        if username == "admin" and password == "admin":
            messages.success(request,'Successfully Login')
            return redirect('admin_index')
        else:
            messages.error(request,'invalid login credentials')
            return redirect('home_admin_login')
    return render(request,"home/home-admin-login.html")


def home_user_login(request):
    if request.method == "POST":
        username=request.POST.get("email")
        password=request.POST.get("password")
        

        try:
            # s1=UserModel.objects.filter(user_status="accepted") | UserModel.objects.filter(user_status="warned")
            auth = UserModel.objects.get(user_email=username,user_password=password)
            if auth.user_status  == "accepted":
                request.session['user_id'] = auth.user_id
                messages.success(request,'Successfully Logged In')
                return redirect('user_index')
            elif auth.user_status == "pending":
                messages.info(request,'Your id is pending for registration ')
                return redirect('home_user_login')
            elif auth.user_status == "blocked":
                messages.error(request,'You Are BLOCKED From Logging In ')
                return redirect('home_user_login')
            else:
                messages.error(request,'You are not registered,try again after signup')
                return redirect('home_user_login')
            
        except:
            messages.error(request,'invalid login credentials')
            return redirect('home_user_login')
    return render(request,"home/home-user-login.html")


def home_user_reg(request):
    
    if request.method == "POST" and request.FILES["license"] and request.FILES["photo"]:
        print('posttt')
        name=request.POST.get("name")
        email=request.POST.get("email")
        contact=request.POST.get("contact")
        password=request.POST.get("password")
        license=request.FILES["license"]
        photo=request.FILES["photo"]
        contact1=request.POST.get("contact1")
        contact2=request.POST.get("contact2")
        contact3=request.POST.get("contact3")
        visibal=request.POST.get("visibal")
        print(name,email,contact,password,license,photo,contact1,contact2,contact3,visibal,"aasdasdasdasdad")


        temp_img=ImgModel.objects.create(image=license)
        temp_img.save()
        
        pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'





        path=str(license)
        print(path,'ttgytg')

        image = cv2.imread('media/temp_img/'+path)
        print(image,'232323434')
        # image resizing  
        resize = cv2.resize(  
            image, None, fx = 2, fy = 2,   
            interpolation = cv2.INTER_CUBIC) 
             
        
        # converting image to grayscale  
        gray = cv2.cvtColor(  
            resize, cv2.COLOR_BGR2GRAY)  
        
        # denoising the image  
        blur = cv2.GaussianBlur(  
            gray, (5, 5), 0) 


        #tesseract
        plate_number = pytesseract.image_to_string(blur, lang ='eng')  
        license_no = "".join(plate_number.split()).replace(":", "").replace("—", "").replace("|SS", "").replace("|", "").replace("Wea", "").replace("=»'", "").replace(")", "").replace("I", "")
        print(license_no,'success')


        #user registeration part
        try:
            s1=UserModel.objects.get(user_license=license_no)
            messages.info(request,"License already exists,try again with another license")
        except:

        
            reg=UserModel.objects.create(user_name=name,user_email=email,user_password=password,user_contact=contact,user_license=license_no,user_photo=photo,user_email_status=contact1,user_sms_status=contact2,user_call_status=contact3,user_privacy_status=visibal)
            reg.save()
            
            if reg:
                messages.success(request,"Registration successful")
                return redirect('home_user_reg')
            else:
                messages.error(request,"invalid details ,try again")
                return redirect('home_user_reg')



    return render(request,"home/home-user-reg.html")



def about(request):
    return render(request,"home/about.html")