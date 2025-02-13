from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from complaint.models import User, Group, Complaint
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from complaint.form import ComplaintForm, UserForm
from django.http import JsonResponse
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import login
from django import forms
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.core.exceptions import PermissionDenied
# Create your views here.

@login_required
def complaint_list(request):
    if not request.user.is_superuser:
        return redirect('permission_denied')
    
    else:
        complaints = Complaint.objects.all()
    
        context = {
            'complaints': complaints
        }

        return render(request, "complaints/complaint_list.html", context)

@login_required
def add_complaint(request):
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to a permission denied page
    else:
        if request.method == 'POST':
            form = ComplaintForm(request.POST)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.save()
                return redirect(reverse('complaint_list') )
        else:
            form = ComplaintForm()

        context = {
            'form': form,
        }

        return render(request, 'complaints/update_complaint.html', context)


@login_required
def update_complaint(request, pk):
    if not request.user.is_superuser:
        return redirect(reverse_lazy('permission_denied')) 
    
    complaint = get_object_or_404(Complaint, id=pk)

    # Restrict access to superusers only
    

    # Handle complaint deletion
    if request.method == "POST" and "delete" in request.POST:
        complaint.delete()
        return redirect(reverse_lazy('sample'))  # Redirect after deletion

    # Process form submission
    form = ComplaintForm(request.POST or None, instance=complaint)
    if form.is_valid():
        form.save()
        return redirect(reverse_lazy('sample'))  # Redirect after successful update

    context = {
        "form": form,
        "complaint": complaint,
        "show_delete_button": True,
    }
    
    return render(request, "complaints/update_complaint.html", context)

@login_required
def customer_complaints(request, user_id):
    # Get the user (User object) based on the user_id
    user = get_object_or_404(User, id=user_id)
    
    # Get complaints related to this user
    complaints = Complaint.objects.filter(customer=user)

    context = {
        'user': user,
        'complaints': complaints,
    }
    
    #ajax
    if request.headers.get('X-Request-With')== + 'XMLHttpRequest':
        complaints = Complaint.objects.annotate(num_complaints = Count('customer_complaints')).values(
            'id','customer', 'item', 'customer_type', 'pick_point', 'appoinment_date', 'complaint_description', 'assigned_to', 'status','technical_report', 'components_used', 'bill_amount'
        )

    return render(request, 'complaints/customer_complaints.html', context)


@login_required
def user_list(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if the request is AJAX
        users = User.objects.annotate(num_complaints=Count('customer_complaints')).values(
            'id', 'username', 'first_name', 'email'
        )

        # Convert QuerySet to list and add user groups
        user_list = []
        for user in users:
            user_obj = User.objects.get(id=user["id"])  # Fetch user object to get groups
            user["groups"] = [group.name for group in user_obj.groups.all()]  # Add groups
            user_list.append(user)

        return JsonResponse({'users': user_list})

    return render(request, 'complaints/user.html')


@login_required
def add_user(request):
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to a permission denied page
    
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('users')  # Change 'home' to the appropriate redirect URL
    else:
        form = UserForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'complaints/update_complaint.html', context)

@login_required
def update_user(request, pk):
    user = get_object_or_404(User, id=pk)
    
    # Check if the logged-in user is a superuser
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to a permission denied page

    # Handle deletion
    if request.method == "POST" and "delete" in request.POST:
        user.delete()
        return redirect(reverse('users'))  # Redirect after deletion
    
    # Handle form submission
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            # If a new password is provided, hash it before saving
            if form.cleaned_data['password']:  
                user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect(reverse('users'))  # Redirect after successful update
    else:
        # Pre-fill the form but do not show the password field
        form = UserForm(instance=user, initial={'password': ''})
        form.fields['password'].widget = forms.HiddenInput()  # Hide the password field

    context = {
        'form': form,
        'user_obj': user,
        'show_delete_button': True,
    }
    
    return render(request, 'complaints/update_user.html', context)


