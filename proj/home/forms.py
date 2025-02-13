from django import forms
from complaint.models import Item, ComplaintStatuses

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
        }


class ComplaintStatusForm(forms.ModelForm):
    class Meta:
        model = ComplaintStatuses
        fields = ['status']