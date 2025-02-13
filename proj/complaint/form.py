from django import forms
from django.contrib.auth.models import User
from complaint.models import Complaint
from django.contrib.auth.hashers import make_password

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['customer', 'item', 'customer_type', 'pick_point', 'appoinment_date', 'complaint_description', 'assigned_to', 'status', 'technical_report', 'components_used', 'bill_amount']
        labels = {
            'customer': 'Phone Number',
            'item': 'Item',
            'customer_type': 'Customer Type',
            'pick_point': 'Pick-up Point',
            'appoinment_date': 'Appointment Date',
            'complaint_description': 'Complaint Description',
            'assigned_to': 'Assigned To',
            'status':'Status',
            'technical_report': 'Technical report',
            'components_used': 'Components Used',
            'bill_amount': 'Billed amount',
            
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'item': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter item'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'pick_point': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter pick-up location'}),
            'appoinment_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'complaint_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter complaint description'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Status'}),
            'technical_report': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Technical Report'}),
            'components_used': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # 'bill_amount': forms.CharField(attrs={'class': 'form-control'})
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make password field optional for updates (not required)
        if self.instance and self.instance.pk:
            self.fields['password'].required = False

    def save(self, commit=True):
    # Save the user object
        user = super().save(commit=False)
    
    # Hash the password before saving
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
    
        if commit:
            user.save()

        # Ensure 'groups' is a list or queryset of groups
            groups = self.cleaned_data['groups']
            if groups:
                user.groups.set(groups)  # Set the groups from the cleaned data
        
            user.save()
    
            return user

    