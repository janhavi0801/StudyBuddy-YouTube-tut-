from django.urls import path
from . import views

urlpatterns = [

    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('user-profile/<str:p>',views.userProfile,name="user-profile"),
    path('',views.home, name="home"),
    path('room/<str:p>',views.room,name="room"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:p>',views.updateRoom,name="update-room"),
    path('delete-room/<str:p>',views.DelRoom,name="delete-room"),
    path('delete-msg/<str:p>',views.Delmsg,name="delete-msg")


]

