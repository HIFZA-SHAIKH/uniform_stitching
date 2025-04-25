from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Order 
from .models import StudentMeasurement  # Ensure this import is correct
from .models import FabricAccessory  # Ensure this model exists

class FabricAccessoryForm(forms.ModelForm):
    class Meta:
        model = FabricAccessory
        fields = ['name', 'quantity', 'unit_price']

class StudentMeasurementForm(forms.ModelForm):
    class Meta:
        model = StudentMeasurement
        fields = ['student_name', 'school_name', 'chest', 'waist', 'height', 'sleeve_length']

class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["measurement", "fabric", "quantity", "status"]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Display student names instead of StudentMeasurement IDs
        self.fields["measurement"].queryset = StudentMeasurement.objects.all()
        self.fields["measurement"].label_from_instance = lambda obj: f"{obj.student_name} ({obj.school_name})"
