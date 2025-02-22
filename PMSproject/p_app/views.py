import datetime
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from p_app.models import Product
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def home_view(request):
    return render(request,"p_app/home.html")

def logout_view(request):
    logout(request)
    return redirect('/login/')

def login_view(request):
    if(request.method== 'POST'):
        un=request.POST.get("un")
        pwd=request.POST.get("pwd")
        user=authenticate(request,username=un,password=pwd)
        if user is None:
            return render(request,"p_app/login.html",{'err' : "Invalid Credentials:.."})
        else:
            login(request,user)
            return redirect("/create/")
    return render(request,"p_app/login.html")

def signup_view(request):
    if(request.method== 'POST'):
        uname=request.POST.get("un")
        pwd=request.POST.get("pwd")
        email=request.POST.get("email")
        print(uname,pwd,email)
        if(User.objects.filter(username=uname).exists()):
            return render(request,"p_app/signup.html", {'err' : "User Already exists:.."})
        else:
            User.objects.create_user(username=uname, email=email,password=pwd)
            return redirect("/login/")
    return render(request,"p_app/signup.html")
@login_required
def create_view(request):
    if(request.method=='POST'):
        pro=Product(pid=request.POST.get('id'),
                  pname=request.POST.get('pname'),
                  price=request.POST.get('pp'),
                  quantity=request.POST.get('qty'),
                  category=request.POST.get('cat'),
                  orderdate=datetime.datetime.now())
        pro.save()
        return redirect('/display/')
    return render(request,"p_app/create.html")

@login_required
def display_view(request):
    db=Product.objects.all()
    return render(request,"p_app/display.html",{'db' : db})


@login_required
def update_view(request,n):
    obj=Product.objects.get(pid=n)
    context={"p" : obj}
    if (request.method=="POST"):
        u_pn=request.POST.get('pname')
        u_r=request.POST.get('pp')
        u_w=request.POST.get('qty')
        u_t=request.POST.get('cat')
        obj.pname=u_pn
        obj.price=u_r
        obj.quantity=u_w
        obj.category=u_t
        obj.save()
        return redirect("/display/")
    print("In Update View", n)
    return render(request,"p_app/update.html",context)

@login_required
def delete_view(request,n):
    obj=Product.objects.get(pid=n)
    obj.delete()
    return redirect("/display/")


@login_required
def filter_view(request):
    if request.method == 'POST':
        pname = request.POST.get('pname')
        cat=request.POST.get('cat')
        pp=request.POST.get('pp')
        db=Product.objects.all()
        if pname:
            db=db.filter(pname__icontains= pname)
        if cat:
            db=db.filter(category__icontains = cat)
        if pp:
            db=db.filter(price__lte = pp)
        context ={
            'db' : db
        }
        return render(request,"p_app/display.html",context)
    elif request.method== 'GET':
        return render(request,"p_app/filter.html")
    else:
        return HttpResponse("An Exception Occured")

