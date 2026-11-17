from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import HostelForm, PaymentForm, RoomForm, StudentForm, VisitorForm, WardenForm
from .models import Hostel, Payment, Room, Student, Visitor, Warden

@login_required
def index(request):
    context = {
        'hostel_count': Hostel.objects.count(),
        'room_count': Room.objects.count(),
        'student_count': Student.objects.count(),
        'payment_count': Payment.objects.count(),
    }
    return render(request, 'index.html', context)
    
@login_required
def student_registration(request):
    message=""
    if request.method == 'POST':
        student_form = StudentForm(request.POST)

        if student_form.is_valid():
            student_form.save()
            message="Student saved successfully."
            
    else:
        student_form = StudentForm()

    students = Student.objects.all()
    student_rows = [
        (student, StudentForm(instance=student))
        for student in students
    ]

    
    context = {
        'student_form': student_form,
        'message': message,
        'student_rows': student_rows,
    }
    return render(request, 'student_registration.html', context)

@login_required
def warden_registration(request):
    message=""
    if request.method == 'POST':
        warden_form = WardenForm(request.POST)

        if warden_form.is_valid():
            warden_form.save()
            message="Warden saved successfully."
        else:
            message="Warden details were not saved. Please correct the errors."

    else:
        warden_form = WardenForm()
    
    wardens = Warden.objects.all()
    warden_rows = [
        (warden, WardenForm(instance=warden))
        for warden in wardens
    ]
    
    context = {
        'warden_form': warden_form,
        'message': message,
        'wardens': wardens,
        'warden_rows': warden_rows,
        'open_add_warden_modal': bool(request.method == 'POST' and warden_form.errors),
    }
    return render(request, 'warden_registration.html', context)

@login_required
def visitor_registration(request):
    message=""
    if request.method == 'POST':
        visitor_form = VisitorForm(request.POST)

        if visitor_form.is_valid():
            visitor_form.save()
            message="Visitor saved successfully."
        else:
            message="Visitor details were not saved. Please correct the errors."

    else:
        visitor_form = VisitorForm()

    visitors = Visitor.objects.all()
    visitor_rows = [
        (visitor, VisitorForm(instance=visitor))
        for visitor in visitors
    ]
    
    context = {
        'visitor_form': visitor_form,
        'message': message,
        'visitors': visitors,
        'visitor_rows': visitor_rows,
        'open_add_visitor_modal': bool(request.method == 'POST' and visitor_form.errors),
    }
    return render(request, 'visitor_registration.html', context)

@login_required
def payment_details(request):
    message=""
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)

        if payment_form.is_valid():
            payment_form.save()
            message="Payment details saved successfully."
        else:
            message="Payment details were not saved. Please correct the errors in the form."

    else:
        payment_form = PaymentForm()
    
    payments = Payment.objects.all()
    payment_rows = [
        (payment, PaymentForm(instance=payment))
        for payment in payments
    ]
    
    context = {
        'payment_form': payment_form,
        'message': message,
        'payments': payments,
        'payment_rows': payment_rows,
        'open_payment_modal': bool(request.method == 'POST' and payment_form.errors),
    }
    return render(request, 'payment_details.html', context)

@login_required
def hostel_details(request):
    message=""
    if request.method == 'POST':
        hostel_form = HostelForm(request.POST)

        if hostel_form.is_valid():
            hostel_form.save()
            message="Hostel details saved successfully."
        else:
            message="Hostel details were not saved. Please correct the errors."
            
    else:
        hostel_form = HostelForm()

    hostels=Hostel.objects.all()
    hostel_rows = [
        (hostel, HostelForm(instance=hostel))
        for hostel in hostels
    ]
    
    context = {
        'hostel_form': hostel_form,
        'message': message,
        'hostels': hostels,
        'hostel_rows': hostel_rows,
        'open_add_hostel_modal': bool(request.method == 'POST' and hostel_form.errors),
    }
    return render(request, 'hostel_details.html', context)

@login_required
def edit_hostel(request, hostel_id):
    if request.method != 'POST':
        return redirect('hostel_details_page')

    hostel = get_object_or_404(Hostel, pk=hostel_id)
    edit_form = HostelForm(request.POST, instance=hostel)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, "Hostel details updated successfully.")
        return redirect('hostel_details_page')

    hostels = Hostel.objects.all()
    hostel_rows = [
        (
            current_hostel,
            edit_form if current_hostel.pk == hostel.pk else HostelForm(instance=current_hostel),
        )
        for current_hostel in hostels
    ]
    context = {
        'hostel_form': HostelForm(),
        'hostels': hostels,
        'hostel_rows': hostel_rows,
        'message': "Please correct the errors in the edit form.",
        'open_edit_hostel_id': hostel.pk,
    }
    return render(request, 'hostel_details.html', context)

@login_required
@require_POST
def delete_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    hostel.delete()
    messages.success(request, "Hostel deleted successfully.")
    return redirect('hostel_details_page')

@login_required
def room_details(request):
    message=""
    if request.method == 'POST':
        room_form = RoomForm(request.POST)

        if room_form.is_valid():
            room_form.save()

            message="Room details saved successfully."
        else:
            message="Room details were not saved. Please correct the errors."

    else:
        room_form = RoomForm()

    rooms = Room.objects.all()
    room_rows = [
        (room, RoomForm(instance=room))
        for room in rooms
    ]
    
    context = {
        'room_form': room_form,
        'message': message,
        'rooms': rooms,
        'room_rows': room_rows,
        'open_add_room_modal': bool(request.method == 'POST' and room_form.errors),
    }
    return render(request, 'room_details.html', context)

@login_required
def edit_room(request, room_id):
    if request.method != 'POST':
        return redirect('room_details_page')

    room = get_object_or_404(Room, pk=room_id)
    edit_form = RoomForm(request.POST, instance=room)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, "Room details updated successfully.")
        return redirect('room_details_page')

    rooms = Room.objects.all()
    room_rows = [
        (
            current_room,
            edit_form if current_room.pk == room.pk else RoomForm(instance=current_room),
        )
        for current_room in rooms
    ]
    context = {
        'room_form': RoomForm(),
        'room_rows': room_rows,
        'message': "Please correct the errors in the edit form.",
        'open_edit_room_id': room.pk,
    }
    return render(request, 'room_details.html', context)

@login_required
@require_POST
def delete_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    room.delete()
    messages.success(request, "Room deleted successfully.")
    return redirect('room_details_page')

@login_required
def edit_visitor(request, visitor_id):
    if request.method != 'POST':
        return redirect('visitor_registration_page')

    visitor = get_object_or_404(Visitor, pk=visitor_id)
    edit_form = VisitorForm(request.POST, instance=visitor)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, "Visitor details updated successfully.")
        return redirect('visitor_registration_page')

    visitors = Visitor.objects.all()
    visitor_rows = [
        (
            current_visitor,
            edit_form if current_visitor.pk == visitor.pk else VisitorForm(instance=current_visitor),
        )
        for current_visitor in visitors
    ]
    context = {
        'visitor_form': VisitorForm(),
        'visitor_rows': visitor_rows,
        'message': "Please correct the errors in the edit form.",
        'open_edit_visitor_id': visitor.pk,
    }
    return render(request, 'visitor_registration.html', context)

@login_required
@require_POST
def delete_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)
    visitor.delete()
    messages.success(request, "Visitor deleted successfully.")
    return redirect('visitor_registration_page')

@login_required
def edit_warden(request, warden_id):
    if request.method != 'POST':
        return redirect('warden_registration_page')

    warden = get_object_or_404(Warden, pk=warden_id)
    edit_form = WardenForm(request.POST, instance=warden)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, "Warden details updated successfully.")
        return redirect('warden_registration_page')

    wardens = Warden.objects.all()
    warden_rows = [
        (
            current_warden,
            edit_form if current_warden.pk == warden.pk else WardenForm(instance=current_warden),
        )
        for current_warden in wardens
    ]
    context = {
        'warden_form': WardenForm(),
        'warden_rows': warden_rows,
        'message': "Please correct the errors in the edit form.",
        'open_edit_warden_id': warden.pk,
    }
    return render(request, 'warden_registration.html', context)

@login_required
@require_POST
def delete_warden(request, warden_id):
    warden = get_object_or_404(Warden, pk=warden_id)
    warden.delete()
    messages.success(request, "Warden deleted successfully.")
    return redirect('warden_registration_page')

@login_required
def edit_payment(request, payment_id):
    if request.method != 'POST':
        return redirect('payment_details_page')

    payment = get_object_or_404(Payment, pk=payment_id)
    edit_form = PaymentForm(request.POST, instance=payment)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, "Payment details updated successfully.")
        return redirect('payment_details_page')

    payments = Payment.objects.all()
    payment_rows = [
        (
            current_payment,
            edit_form if current_payment.pk == payment.pk else PaymentForm(instance=current_payment),
        )
        for current_payment in payments
    ]
    context = {
        'payment_form': PaymentForm(),
        'payment_rows': payment_rows,
        'message': "Please correct the errors in the edit form.",
        'open_edit_payment_id': payment.pk,
    }
    return render(request, 'payment_details.html', context)

@login_required
@require_POST
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    payment.delete()
    messages.success(request, "Payment deleted successfully.")
    return redirect('payment_details_page')

@login_required
def edit_student(request, student_id):
    if request.method != 'POST':
        return redirect('student_registration_page')

    student = get_object_or_404(Student, pk=student_id)
    edit_form = StudentForm(request.POST, instance=student)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, "Student details updated successfully.")
        return redirect('student_registration_page')

    students = Student.objects.all()
    student_rows = [
        (
            current_student,
            edit_form if current_student.pk == student.pk else StudentForm(instance=current_student),
        )
        for current_student in students
    ]
    context = {
        'student_form': StudentForm(),
        'student_rows': student_rows,
        'message': "Please correct the errors in the edit form.",
        'open_edit_student_id': student.pk,
    }
    return render(request, 'student_registration.html', context)

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return redirect('student_registration_page')

def signup(request):
    message = ""
    if request.method == 'POST':
        sign_up_form = UserCreationForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            message = "User created successfully."
        else:
            message = "Something went wrong."
            
    else:
        sign_up_form = UserCreationForm()

    context = {
        'sign_up_form': sign_up_form,
        'message': message
    }
    return render(request, 'registration/sign_up.html', context)
