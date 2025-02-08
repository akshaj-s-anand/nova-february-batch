from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from complaint.models import User, Group, Complaint
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from complaint.form import ComplaintForm, UserForm
from django.http import JsonResponse
from django.db.models import Count
# Create your views here.

@login_required
def sample(request):
    
    user = User.objects.all()
    # customers = User.objects.filter(groups__id=1)
    complaint = Complaint.objects.all()

    
    context = {
        'users': user,
        # 'customers':customers,
        'complaint':complaint,
    }
    
    return render (request, 'complaints/sample.html', context)

@login_required
def add_complaint(request):
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to a permission denied page
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.save()
            return redirect(reverse('sample') )
    else:
        form = ComplaintForm()

    context = {
        'form': form,
    }

    return render(request, 'complaints/update_complaint.html', context)


@login_required
def update_complaint(request, pk):
    complaint = get_object_or_404(Complaint, id=pk)
    
    # Check if the user is a superuser
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to permission denied page
    
    # If 'delete' button is pressed
    if 'delete' in request.POST:
        complaint.delete()  # Delete the complaint
        return redirect(reverse('sample'))  # Redirect to another page after deletion
    
    # Handling form submission
    form = ComplaintForm(request.POST or None, instance=complaint)
    if form.is_valid():
        form.save()  # Save the updated complaint
        return redirect(reverse('sample'))  # Redirect after successful update
    
    context = {
        'form': form,
        'complaint': complaint,
        'show_delete_button': True, 
    }
    
    return render(request, 'complaints/update_complaint.html', context)

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

    return render(request, 'complaints/customer_complaints.html', context)

@login_required
def user(request):
    # Annotate each user with the total number of complaints
    users = User.objects.annotate(num_complaints=Count('customer_complaints'))
    
    context = {
        'users': users,
    }
    
    return render(request, 'complaints/user.html', context)

@login_required
def add_user(request):
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to a permission denied page
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('users'))  # Redirect to users list page after creation
    else:
        form = UserForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'complaints/update_complaint.html', context)

@login_required
def update_user(request, pk):
    user = get_object_or_404(User, id=pk)
    
    # Check if the user is a superuser
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to permission denied page
    
    # If 'delete' button is pressed
    if 'delete' in request.POST:
        user.delete()  # Delete the complaint
        return redirect(reverse('users'))  # Redirect to another page after deletion
    
    # Handling form submission
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()  # Save the updated complaint
        return redirect(reverse('users'))  # Redirect after successful update
    
    context = {
        'form': form,
        'complaint': user,
        'show_delete_button': True, 
    }
    
    return render(request, 'complaints/update_complaint.html', context)



