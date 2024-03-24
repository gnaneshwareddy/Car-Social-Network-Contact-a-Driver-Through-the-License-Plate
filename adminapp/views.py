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
from django.core.paginator import Paginator
# Create your views here.





def admin_index(request):
    pending=UserModel.objects.filter(user_status="pending").count()
    all=UserModel.objects.all().count()
    reviews= FeedbackModel.objects.all().count()
    a=InteractionModel.objects.values_list('from_user', 'to_user').distinct()
    

    global k
    k=[]

    for i in a:
        
        
        
        b=i[0]
        c=i[1]
        
        d=InteractionModel.objects.filter(from_user = b,to_user = c)[0]
        k+=[d]
    c=0
    for i  in k:
        c+=1
    
    

    return render(request,"admin/admin-index.html",{'pend':pending,'all':all,'rev':reviews,'interac':c})


def admin_pending_users(request):
    pending=UserModel.objects.filter(user_status="pending")
    paginator = Paginator(pending,5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    
    return render(request,"admin/admin-pending-users.html",{'pend':page})


def admin_all_users(request):
    all=UserModel.objects.all().order_by('-datetime_created')
    paginator = Paginator(all,5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    return render(request,"admin/admin-all-users.html",{'all':page})




def admin_interactions(request):
    q=InteractionModel.objects.all()
    # email_list = InteractionModel.objects.values_list('from_user').distinct()
    a=InteractionModel.objects.values_list('from_user', 'to_user').distinct()
    

    global o
    o=[]

    for i in a:
        
        
        
        b=i[0]
        c=i[1]
        
        d=InteractionModel.objects.filter(from_user = b,to_user = c)[0]
        o+=[d]
    paginator = Paginator(o,5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)

    return render(request,"admin/admin-interactions.html",{'o':page})


def admin_user_feedback(request):
    feedback= FeedbackModel.objects.all()
    reviews=FeedbackModel.objects.filter()
    paginator = Paginator(feedback,5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    return render(request,"admin/admin-user-feedback.html",{'feed':page})


def admin_sentiment_analysis(request):
    pos=FeedbackModel.objects.filter(sentiment="positive").count()
    neu=FeedbackModel.objects.filter(sentiment="neutral").count()
    neg=FeedbackModel.objects.filter(sentiment="negative").count()
    return render(request,"admin/admin-sentiment-analysis.html",{'pos':pos,'neu':neu,'neg':neg})


def accept_user(request,user_id):
    accept = get_object_or_404(UserModel,user_id=user_id)
    accept.user_status = "accepted"
    accept.save(update_fields=["user_status"])
    accept.save()
    if accept:
        messages.success(request,"User Added Successfully")

    return redirect('admin_pending_users')

def decline_user(request,user_id):
    decline = get_object_or_404(UserModel,user_id=user_id)
    decline.user_status = "declined"
    decline.save(update_fields=["user_status"])
    decline.save()
    if decline:
        messages.success(request,"Rejected Successfully")

    return redirect('admin_pending_users')