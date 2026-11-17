from django.contrib import admin

from .models import Hostel, Room, Student, Warden, Visitor, Payment

class HostelAdmin(admin.ModelAdmin):
    list_display = ('hostel_name', 'hostel_id', 'location', 'capacity', 'status')
    search_fields = ('hostel_name', 'hostel_id', 'location')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'room_number', 'hostel_id', 'capacity', 'status')
    search_fields = ('room_id', 'room_number', 'hostel_id')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'room_id', 'birth_date', 'gender', 'course', 'contact')
    search_fields = ('student_id', 'first_name', 'last_name', 'room_id')

class WardenAdmin(admin.ModelAdmin):
    list_display = ('warden_id', 'first_name', 'last_name', 'hostel_id', 'contact')
    search_fields = ('warden_id', 'first_name', 'last_name', 'hostel_id')

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor_id', 'first_name', 'last_name', 'relation_to_student', 'date_of_visit', 'intime', 'outtime', 'contact', 'address')
    search_fields = ('visitor_id', 'first_name', 'last_name', 'relation_to_student')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'student_id', 'amount', 'date_of_payment', 'mode_of_payment', 'due_date', 'status', 'academic_year', 'semester')
    search_fields = ('payment_id', 'student_id')

admin.site.register(Hostel, HostelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Warden, WardenAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Payment, PaymentAdmin)
