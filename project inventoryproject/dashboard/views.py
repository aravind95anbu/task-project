from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request,'dashboard/index.html')



def staff(request):
    return render (request,'staff.html')
def user_register_view(request):
    
    return HttpResponse("User registration page")
