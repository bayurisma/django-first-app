from email import message
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from wishlist.models import BarangWishlist
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from .forms import WishlistForm
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='/wishlist/login/')
def show_wishlist(req):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
        'list_barang': data_barang_wishlist,
        'nama': 'Bayu Risma',
        'last_login': req.COOKIES['last_login'],
    }
    return render(req, "wishlist.html", context)


def return_xml(req):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def return_json(req):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def return_json_by_id(req, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def return_xml_by_id(req, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def register(req):
    form = UserCreationForm()

    if req.method == "POST":
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
        
    context = {'form':form}
    return render(req, 'register.html', context)

def login_user(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            res = HttpResponseRedirect(reverse("wishlist:show_wishlist"))
            res.set_cookie('last_login', str(datetime.datetime.now()))
            return res
        else:
            messages.info(req, 'Username atau Password salah!')
    
    context = {}
    return render(req, 'login.html', context)

def logout_user(req):
    logout(req)
    res = HttpResponseRedirect(reverse('wishlist:login'))
    res.delete_cookie('last_login')
    return res

@login_required(login_url='/wishlist/login/')
def getData(req):     
    context = {
        'nama': 'Bayu Risma',
        'last_login': req.COOKIES['last_login'],
    }
    return render(req, 'wishlist_ajax.html', context)

@login_required(login_url="/wishlist/login/")
def ajaxForm(req):
    if req.method == "POST":
        nama_barang = req.POST.get("nama_barang")
        harga_barang = req.POST.get("harga_barang")
        deskripsi = req.POST.get("deskripsi")
        newItem = BarangWishlist(
            nama_barang=nama_barang, harga_barang=harga_barang, deskripsi=deskripsi
        )
        newItem.save()
        JsonResponse({}, status=200)
    
    return redirect("wishlist:getData")
