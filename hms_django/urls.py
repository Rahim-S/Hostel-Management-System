"""
URL configuration for hostel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from hostel.views import index,student_registration, warden_registration, visitor_registration, payment_details,room_details, hostel_details, edit_hostel, delete_hostel, edit_room, delete_room, edit_visitor, delete_visitor, edit_warden, delete_warden, edit_payment, delete_payment, edit_student, delete_student, signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index_page'),
    path('student_registration/', student_registration, name='student_registration_page'),
    path('warden_registration/', warden_registration, name='warden_registration_page'),
    path('visitor_registration/', visitor_registration, name='visitor_registration_page'),
    path('payment_details/', payment_details, name='payment_details_page'),
    path('room_details/', room_details, name='room_details_page'),
    path('hostel_details/', hostel_details, name='hostel_details_page'),
    path('edit_hostel/<int:hostel_id>/', edit_hostel, name='edit_hostel_page'),
    path('delete_hostel/<int:hostel_id>/', delete_hostel, name='delete_hostel_page'),
    path('edit_room/<int:room_id>/', edit_room, name='edit_room_page'),
    path('delete_room/<int:room_id>/', delete_room, name='delete_room_page'),
    path('edit_visitor/<int:visitor_id>/', edit_visitor, name='edit_visitor_page'),
    path('delete_visitor/<int:visitor_id>/', delete_visitor, name='delete_visitor_page'),
    path('edit_warden/<int:warden_id>/', edit_warden, name='edit_warden_page'),
    path('delete_warden/<int:warden_id>/', delete_warden, name='delete_warden_page'),
    path('edit_payment/<int:payment_id>/', edit_payment, name='edit_payment_page'),
    path('delete_payment/<int:payment_id>/', delete_payment, name='delete_payment_page'),
    path('edit_student/<int:student_id>/', edit_student, name='edit_student_page'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student_page'),
    path('sign_up/', signup, name='sign_up_page'),
    path('accounts/',include('django.contrib.auth.urls')),
]
