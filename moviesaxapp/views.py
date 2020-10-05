from django.shortcuts import render

# Create your views here.
from django.http import  HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import  requests
from django.http import HttpResponse, JsonResponse
from .backend.movie_query import MovieQuery
import ipfshttpclient
import threading
from django.utils.safestring import mark_safe
import os
import time
import traceback

def index(request):
    context = {'user_signed_in': False}
    return  render(request, 'frontpage/index.html', context)



def signup(request):
    context = {'user_signed_in': False}
    if request.method == 'POST':
        user = request.POST['email']
        pwd = request.POST['pwd']
        user_obj = User.objects.create_user(user,user,pwd)
        user_obj.save()
        auth_user = authenticate(username=user, password = pwd)
        login(request,auth_user)
        return redirect("/")
    else:
        return  render(request, 'account/signup.html', context)

def signin(request):
    context = {}
    if request.method == 'POST':
        user = request.POST['email']
        pwd = request.POST['pwd']
        auth_user = authenticate(username=user, password=pwd)
        if auth_user is not None:
            msg = "success authenticated"
            print(msg)
            login(request, auth_user)
            return  redirect("/")
        else:
            msg ="Login failed"
            context = {'msg': msg}
            print(msg)
            return redirect("/signin")
    else:
        return  render(request, 'account/signin.html', context)

def forgotpass(request):
    context = {}
    return  render(request, 'account/forgotpass.html', context)

@login_required(login_url='/signin')
def test(request):
    context = {}
    return  render(request, 'base.html', context)

@login_required(login_url='/signin')
def signout(request):
    logout(request)
    return redirect("/")

def products(request):
    context = {'user_signed_in': False}
    return  render(request, 'frontpage/products.html', context)

def services(request):
    context = {'user_signed_in': False}
    return  render(request, 'frontpage/services.html', context)


def aboutus(request):
    context = {'user_signed_in': False}
    return  render(request, 'frontpage/aboutus.html', context)

def testvideo(request):
    context = {'user_signed_in': False}
    return render(request,'frontpage/video.html',context)

def viewvideo(request,cid,name):
    print("cid=" + cid + ", name = " + name)
    context = {'user_signed_in': False}
    context["cid"] = cid
    context["name"] = name
    context["video_url"] = "/video/"+ cid + "/" + name
    video_file_with_cid = os.path.join("moviesaxapp/static/video", cid)
    video_file_with_path_cid_name = os.path.join(video_file_with_cid, name)

    if os.path.exists(video_file_with_path_cid_name):
        print("File " + video_file_with_path_cid_name + " exist")
        return render(request, 'frontpage/video.html', context)
    else:
        print("Process video file ")
        t = threading.Thread(target=download_ipfs_video,args=(cid, video_file_with_cid, name,))
        t.start()
        # time.sleep(10)
        #download_ipfs_video(cid, video_file_with_cid, name)
        #print("Process video done")
        return render(request,'frontpage/loading.html')


def video_cid(request):
    context = {'user_signed_in': False}
    if request.method == 'GET':
        tmp_arr =MovieQuery.get_movies_cid()
        return JsonResponse(tmp_arr,safe=False)





def download_ipfs_video(cid, video_file_with_cid, name):
    try:
        with ipfshttpclient.connect() as client:
            client.get(cid,video_file_with_cid)
        org_file = os.path.join(video_file_with_cid, cid)
        new_file = os.path.join(video_file_with_cid,name)
        print("Change from " + str(org_file) + " to: " + str(new_file))
        os.rename(org_file,new_file)
        print("Change name done")
    except:
        print("Fail to get video " + str(traceback.print_exc()))

