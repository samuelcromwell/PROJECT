from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('', views.base, name="base"),
    path('logout/',views.logoutUser, name="logout"),   
    path('profile/',views.profile, name="profile"),
    path('timetable/',views.fullcalendar, name="fullcalendar"),
    path('payments/',views.payments, name="payments"),   
    path('book/',views.book, name="book"),      
    path('profile/edit',views.edit, name="edit"),   
    path('profile/changepassword',views.change, name="change"), 
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),   
    path('printpayments/',views.print_payments, name="printpayments"), 
    path('printschedule/',views.print_schedule, name="printschedule"), 
    path('book_event/<int:event_id>/', views.book_event, name='book_event'),
    path('events/', views.showlessons, name='event_list'),   
    path('printprofile/', views.print_profile, name='printprofile'),   
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('calendarschedule/',views.calendarschedule, name="calendarschedule"),   
]