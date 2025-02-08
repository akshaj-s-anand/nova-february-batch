from django import forms
from django.contrib.auth.models import User
from complaint.models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['customer', 'item', 'customer_type', 'pick_point', 'appoinment_date', 'assigned_to']
        labels = {
            'customer': 'Customer Name',
            'item': 'Item',
            'customer_type': 'Customer Type',
            'pick_point': 'Pick-up Point',
            'appoinment_date': 'Appointment Date',
            'assigned_to': 'Assigned To',
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'item': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter item'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'pick_point': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter pick-up location'}),
            'appoinment_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'appoinment_date': 'Select a valid date for the appointment.',
        }
        error_messages = {
            'item': {
                'required': 'This field is required.',
            },
            'pick_point': {
                'required': 'This field is required.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter the 'assigned_to' field based on user groups 2 and 3
        self.fields['assigned_to'].queryset = User.objects.filter(groups__id__in=[2, 3])
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'groups']
        labels = {
            'username': 'Phone Number',
            'email': 'Email ID',
            'password': 'Password',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'is_staff': 'Staff Status',
            'is_active': 'Active Status',
            'date_joined': 'Date Joined',
            'groups': 'Groups',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_joined': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }