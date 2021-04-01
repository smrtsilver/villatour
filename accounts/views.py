from django.shortcuts import render,get_object_or_404


# Create your views here.
from accounts.models import *


def landing(request):
    return render(request,"landing/index.html")
def profileview(request,profileToken):
    # return render()
    amlakObj=get_object_or_404(realstateModel,pk=profileToken)

    context={
        "amlak" : amlakObj
    }
    return render(request,"accounts/profile.html",context=context)
