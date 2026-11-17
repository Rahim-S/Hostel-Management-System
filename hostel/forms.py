from django.forms import DateInput, ModelForm
from .models import Hostel, Room, Student, Warden, Visitor, Payment

class HostelForm(ModelForm):
    class Meta:
        model = Hostel
        fields = '__all__'

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class WardenForm(ModelForm):
    class Meta:
        model = Warden
        fields = '__all__'

class VisitorForm(ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'date_of_payment': DateInput(attrs={'type': 'date'}),
            'due_date': DateInput(attrs={'type': 'date'}),
        }
