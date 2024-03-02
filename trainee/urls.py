from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

urlpatterns = [
    path('', views.base, name="base"),
    path('logout/',views.logoutUser, name="logout"),   
    path('profile/',views.profile, name="profile"),   
    path('payments/',views.payments, name="payments"),   
    path('profile/edit',views.edit, name="edit"),   
    path('profile/changepassword',views.change, name="change"), 
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    
]