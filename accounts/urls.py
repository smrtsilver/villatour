from django.urls import path

from accounts import views

urlpatterns = [
    path("profile/<int:profileToken>",views.profileview,name="profiledetail"),
    path("landing/",views.landing)
]