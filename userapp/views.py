from ast import Return
from email.message import Message

# from ssl import _PasswordType
from django.db.models import Avg,Max,Min,Sum,Count,StdDev,Variance
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from adminapp.models import *
from mainapp.models import *
from userapp.models import *
import pytesseract
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import imutils
import cv2
import os
from car_social_network.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives
import requests
import pathlib
from django.core.files.storage import FileSystemStorage
import socket
from django.core.paginator import Paginator
# Create your views here.


def user_index(request):
    
    if request.method == "POST" and request.FILES["license"]:
        
        plate_img=request.FILES["license"]
        

        #License plate number is extracted from image here!
        # temp_img=ImgModel.objects.create(image=plate_img)
        # temp_img.save()
        
        pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'





        path=str(plate_img)
        

        image = cv2.imread('media/temp_img/'+path)
        
        # image resizing
        try:  
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
            license_no = "".join(plate_number.split()).replace(":", "").replace("—", "").replace("|SS", "").replace("|", "").replace("Wea", "").replace("=»'", "").replace(")", "").replace("I", "").replace("_", "").replace("-", "").replace("(", "").replace("‘", "")
            


            try:
                driver = UserModel.objects.get(user_license= license_no) 
                
                # return redirect('user_index')
            except:
                messages.info(request, 'No Driver Found')
                return redirect('user_index')
            return render(request,"user/user-index.html",{'driver':driver})
        except:
            messages.info(request, 'No Driver Found With This Plate')
    return render(request,"user/user-index.html")


# def user_com(request):
#     if request.method =="POST":
#         message=request.POST.get("message")
#         print(message,"comm message")
#     return render(request,"user/user-com.html")


def user_interactions(request):
    user_id=request.session['user_id']
    my_inter = InteractionModel.objects.filter(from_user = user_id)
    paginator = Paginator(my_inter,5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    return render(request,"user/user-interactions.html",{'a':page})



def user_profile(request):
    user_id=request.session['user_id']
    user=UserModel.objects.get(user_id=user_id)
    # device=DeviceModel.objects.filter(device_user=user_id).count()

    
    if request.method=="POST":
        if len(request.FILES) ==0:
            name=request.POST.get("name")
            
            email=request.POST.get("email")
            password=request.POST.get("password")
            contact=request.POST.get("contact")
            privacy = request.POST.get("privacy")
            license = request.POST.get("license")
            # photo=request.FILES["photo"]
            user.user_name = name
            
            user.user_email = email
            user.user_password = password
            user.user_contact = contact
            user.user_privacy_status =  privacy
            user.user_license = license
        # user.user_country = country

            user.save()
            if user:
                messages.success(request,"Succesflly Updated")
                return redirect("user_profile")

            else:
                messages.error(request,"No changes detected")
                return redirect("user_profile")
        else:
            if request.method=="POST" and request.FILES['file']:
                profile=request.FILES['file']
                name=request.POST.get("name")
                
                email=request.POST.get("email")
                password=request.POST.get("password")
                contact=request.POST.get("contact")
                privacy = request.POST.get("privacy")
                license = request.POST.get("license")
                # photo=request.FILES["photo"]
                user.user_name = name
                user.user_photo = profile
                user.user_email = email
                user.user_password = password
                user.user_contact = contact
                user.user_privacy_status =  privacy
                user.user_license = license
                
                # user.user_country = country

                user.save()
                if user:
                    messages.success(request,"Succesflly Updated")
                    return redirect("user_profile")
                

                    

                else:
                    messages.error(request,"No changes detected")
                    return redirect("user_profile")
    return render(request,"user/user-profile.html",{'user':user})



def user_feedback(request):
    user_id=request.session['user_id']
    user=UserModel.objects.get(user_id=user_id)
    if request.method == "POST":
        rating=request.POST.get("rating")
        review=request.POST.get("review")
        sid_obj= SentimentIntensityAnalyzer()
        sentinent = sid_obj.polarity_scores(review)
        
        if sentinent["compound"] > 0:
            sent = "positive"
        elif sentinent["compound"] < 0:
            sent = "negative"

        else:
            sent = "neutral"

        if sent:
            feedback = FeedbackModel.objects.create(review=review,rating=rating,reviewer=user,sentiment=sent)
            feedback.save()
            messages.success(request,"Your review has been added succesfully.")
            
            
            return redirect('user_feedback')

        else:
            
            messages.info(request,"You have already reviewed this driver.")
            return redirect('user_feedback')

       
    
    return render(request,"user/user-feedback.html")



def contact_email(request,driver_id,text):
    user_id=request.session['user_id']
    user=UserModel.objects.get(user_id=user_id)
    u1=user.user_id
    
    
    driver=UserModel.objects.get(user_id=driver_id)
    d1=driver.user_id
    if request.method =="POST":
        message = request.POST.get("message")
        
        if text == 'email':
            #email integration
            html_content = "<p>From:&nbsp;"+user.user_name+"</p>"+"<br>"+message+"."
            from_mail = DEFAULT_FROM_EMAIL

            to_mail = [driver.user_email]
            
            msg = EmailMultiAlternatives(
                "Car Social Network", html_content, from_mail, to_mail)
            msg.attach_alternative(html_content, "text/html")
            print(html_content,from_mail,to_mail,msg,'asdasdasdasdsdd')
            msg.send()
            if msg:
                InteractionModel.objects.create(message=message,interac_type =text,to_user=driver,from_user=user)
                print('ededededed')
                messages.success(request, 'Email Sent Successfully')
                return redirect('contact_email',driver_id=driver_id,text=text)
            
        elif text == 'sms':
            #SMS API CODE
                
                url = "https://www.fast2sms.com/dev/bulkV2"
                # create a dictionary
                my_data = {'sender_id': 'FSTSMS', 
                                'message': 'From '+user.user_name+','+message,
                                'language': 'english', 
                                'route': 'q', 
                                'numbers':8328035152,
                }
                
                    # create a dictionary
                headers = {
                        'authorization': "Ns8H1mKg294AjeBz5DMxLhPaZrbFR7tfpk3EX6wYJWUqd0noiGlHUTm1nDyEaCpx38R45MtKJg9kG6iB",
                        'Content-Type': "application/x-www-form-urlencoded",
                        'Cache-Control': "no-cache"
                }
                    # make a post request
                response = requests.request("POST",url,data = my_data,headers=headers)
                # print(response.text,"sms message")
                
                sms=InteractionModel.objects.create(message=message,interac_type =text,to_user=driver,from_user=user)
                messages.success(request, 'Sms Sent Successfully')

                
                return redirect('contact_email',driver_id=driver_id,text=text)
        

    return render(request,"user/user-com.html",{'driver':driver_id,'text':text})


def contact_call(request,driver_id,text):
    user_id=request.session['user_id']
    user=UserModel.objects.get(user_id=user_id)
    u1=user.user_id
    driver=UserModel.objects.get(user_id=driver_id)
    
    d1=driver.user_id

    
            #call integration
    calls=InteractionModel.objects.create(message="call",interac_type =text,to_user=driver,from_user=user)
    
    if calls:
    
        
        messages.success(request,"Call Made Successfully")
        return redirect('user_index')
    
    else:
        messages.error(request,"Something went wrong")
        return redirect('user_index')
    return render(request,"user/user-index.html")

# def contact_sms(request,driver_id,sms):
#     user_id=request.session['user_id']
#     user=UserModel.objects.get(user_id=user_id)
#     driver=UserModel.objects.get(user_id=driver_id)
#     if request.method =="POST":
#         message = request.POST.get("message")
#         print(message,"sms message")

    

    

#     return render(request,"user/user-com.html")

#review from user
# def review(request,driver_id):
#     user_id=request.session['user_id']
#     user=UserModel.objects.get(user_id=user_id)
#     driver=UserModel.objects.get(user_id=driver_id)
#     if  request.method=="POST":
#         rating = request.POST.get("rating")
#         review = request.POST.get("review")
#         sid_obj= SentimentIntensityAnalyzer()
#         sentinent = sid_obj.polarity_scores(review)
        
#         if sentinent["compound"] > 0:
#             sent = "positive"
#         elif sentinent["compound"] < 0:
#             sent = "negative"

#         else:
#             sent = "neutral"

#         try:
#             a=FeedbackModel.objects.get(reviewer=user_id,reviewee=driver_id)
#             messages.info(request,"You have already reviewed this driver.")
#             print(a)
#             return redirect('review',driver_id=driver_id)

#         except:
#             feedback = FeedbackModel.objects.create(review=review,rating=rating,reviewer=user,reviewee=driver,sentinent=sent)
#             feedback.save()
#             messages.success(request,"Your review has been added succesfully.")
#             return redirect('review',driver_id=driver_id)

#     return render(request,"user/user-feedback.html")